import io
import os
import tempfile
import pytest
from flask import Flask
from werkzeug.datastructures import FileStorage
from unittest.mock import patch

# NOTE: This is a test skeleton for file upload and parsing logic.
# It assumes you will implement endpoints like /upload_rulebook and parsing utilities.
# Adjust import paths and endpoint names as needed for your actual implementation.

SUPPORTED_TYPES = [
    (b"%PDF-1.4\n...", "test.pdf", "application/pdf"),
    (b"PK\x03\x04...docx...", "test.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    (b"This is a plain text rulebook.", "test.txt", "text/plain"),
]

UNSUPPORTED_TYPES = [
    (b"\xff\xd8\xff...", "test.jpg", "image/jpeg"),
    (b"MZ...", "test.exe", "application/octet-stream"),
    (b"...xls...", "test.xls", "application/vnd.ms-excel"),
]

def upload_file(client, file_bytes, filename, content_type):
    data = {
        'file': (io.BytesIO(file_bytes), filename)
    }
    return client.post('/upload_rulebook', data=data, content_type='multipart/form-data')

def test_upload_supported_types(client):
    for file_bytes, filename, content_type in SUPPORTED_TYPES:
        resp = upload_file(client, file_bytes, filename, content_type)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get('success') or data.get('rules')

def test_upload_unsupported_types(client):
    for file_bytes, filename, content_type in UNSUPPORTED_TYPES:
        resp = upload_file(client, file_bytes, filename, content_type)
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'error' in data
        assert 'unsupported' in data['error'].lower()

def test_upload_empty_file(client):
    resp = upload_file(client, b"", "empty.pdf", "application/pdf")
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data
    assert 'empty' in data['error'].lower()

def test_upload_too_large_file(client):
    # Simulate a file >50MB
    big_file = b"0" * (50 * 1024 * 1024 + 1)
    resp = upload_file(client, big_file, "big.pdf", "application/pdf")
    assert resp.status_code == 413 or resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data
    assert 'size' in data['error'].lower() or 'too large' in data['error'].lower()

# PDF Parsing
@patch('backend.utils.parse_pdf')
def test_parse_pdf_text(mock_parse_pdf, client):
    mock_parse_pdf.return_value = {'text': 'Combat\nEquipment', 'sections': ['Combat', 'Equipment'], 'tables': []}
    resp = upload_file(client, b"%PDF-1.4\n...", "test.pdf", "application/pdf")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Combat' in data.get('rules', '')
    assert 'sections' in data
    assert 'tables' in data

@patch('backend.utils.parse_pdf')
def test_parse_pdf_tables(mock_parse_pdf, client):
    mock_parse_pdf.return_value = {'text': '...', 'sections': [], 'tables': [{'name': 'Gear', 'rows': [["Sword", "10gp"]]}]}
    resp = upload_file(client, b"%PDF-1.4\n...", "test.pdf", "application/pdf")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any('Gear' in t.get('name', '') for t in data.get('tables', []))

@patch('backend.utils.parse_pdf')
def test_parse_pdf_with_images(mock_parse_pdf, client):
    mock_parse_pdf.return_value = {'text': 'Text only', 'sections': [], 'tables': []}
    resp = upload_file(client, b"%PDF-1.4\n...", "test.pdf", "application/pdf")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Text only' in data.get('rules', '')

@patch('backend.utils.parse_pdf')
def test_parse_encrypted_pdf(mock_parse_pdf, client):
    mock_parse_pdf.side_effect = Exception('Encrypted PDF')
    resp = upload_file(client, b"%PDF-1.4\n...", "locked.pdf", "application/pdf")
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'encrypted' in data['error'].lower() or 'locked' in data['error'].lower()

# DOCX Parsing
@patch('backend.utils.parse_docx')
def test_parse_docx_text(mock_parse_docx, client):
    mock_parse_docx.return_value = {'text': 'Header\nList', 'sections': ['Header'], 'tables': []}
    resp = upload_file(client, b"PK\x03\x04...docx...", "test.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Header' in data.get('rules', '')
    assert 'sections' in data

@patch('backend.utils.parse_docx')
def test_parse_docx_tables(mock_parse_docx, client):
    mock_parse_docx.return_value = {'text': '...', 'sections': [], 'tables': [{'name': 'Stats', 'rows': [["HP", "10"]]}]}
    resp = upload_file(client, b"PK\x03\x04...docx...", "test.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any('Stats' in t.get('name', '') for t in data.get('tables', []))

# TXT Parsing
def test_parse_txt_text(client):
    resp = upload_file(client, b"Combat\n\nEquipment\n--\nStats", "test.txt", "text/plain")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Combat' in data.get('rules', '')
    assert 'Equipment' in data.get('rules', '')

def test_parse_txt_sections(client):
    resp = upload_file(client, b"Section1\n\nSection2\n==\nSection3", "test.txt", "text/plain")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Section1' in data.get('rules', '')
    assert 'Section2' in data.get('rules', '')
    assert 'Section3' in data.get('rules', '')

# Error Handling
def test_parse_unusual_characters(client):
    resp = upload_file(client, "Café ☃️ — Δ".encode("utf-8"), "test.txt", "text/plain")
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Café' in data.get('rules', '')

def test_parse_malformed_file(client):
    # Simulate a file with some unreadable bytes
    resp = upload_file(client, b"Good\n\xff\xfe\x00\x00Bad", "test.txt", "text/plain")
    assert resp.status_code == 200 or resp.status_code == 400
    data = resp.get_json()
    if resp.status_code == 200:
        assert 'Good' in data.get('rules', '')
    else:
        assert 'error' in data

def test_multiple_file_uploads(client):
    # Upload two files in sequence
    resp1 = upload_file(client, b"Combat", "file1.txt", "text/plain")
    resp2 = upload_file(client, b"Equipment", "file2.txt", "text/plain")
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    data1 = resp1.get_json()
    data2 = resp2.get_json()
    assert 'Combat' in data1.get('rules', '')
    assert 'Equipment' in data2.get('rules', '')

def test_output_formatting(client):
    resp = upload_file(client, b"Combat\nEquipment", "test.txt", "text/plain")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data.get('rules'), str) or isinstance(data.get('rules'), dict)

def test_error_logging(client, caplog):
    with caplog.at_level('ERROR'):
        resp = upload_file(client, b"", "empty.pdf", "application/pdf")
        assert resp.status_code == 400
        assert any('empty' in r.getMessage().lower() for r in caplog.records)

def test_rulebook_deduplication(client):
    # Upload the same file twice, should not be parsed/scanned twice
    file_bytes = b"Combat\nEquipment"
    resp1 = upload_file(client, file_bytes, "dedupe.txt", "text/plain")
    resp2 = upload_file(client, file_bytes, "dedupe.txt", "text/plain")
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    data1 = resp1.get_json()
    data2 = resp2.get_json()
    assert data1.get('rules') == data2.get('rules')
    # Optionally, check a log or counter to ensure only one parse occurred
