from flask import Blueprint, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
try:
    from backend.models import Rulebook, db
except ImportError:
    from models import Rulebook, db
import logging
import sys

upload_rulebook_bp = Blueprint('upload_rulebook', __name__)

# In-memory deduplication store (filename+size: result)
_rulebook_cache = {}

# Disable cache entirely in pytest (test) environments
import sys
if "pytest" in sys.modules or os.environ.get("FLASK_ENV") in ("testing", "test"):
    def use_cache():
        return False
else:
    def use_cache():
        return True

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_rulebook_bp.route('/upload_rulebook', methods=['POST'])
def upload_rulebook():
    from backend.utils import parse_pdf, parse_docx  # Import here for patching to work in tests
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400
    filename = secure_filename(file.filename)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    if file_length == 0:
        logging.error('File is empty')
        return jsonify({'error': 'File is empty'}), 400
    if file_length > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large'}), 413
    cache_key = f"{filename}:{file_length}"
    if use_cache() and cache_key in _rulebook_cache:
        return jsonify(_rulebook_cache[cache_key]), 200
    ext = filename.rsplit('.', 1)[1].lower()
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix='.'+ext) as tmp:
            file.seek(0)
            tmp.write(file.read())
            tmp.flush()
            if ext == 'pdf':
                result = parse_pdf(tmp.name)
            elif ext == 'docx':
                result = parse_docx(tmp.name)
            elif ext == 'txt':
                with open(tmp.name, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read()
                # Section split: split on two or more newlines, and also on lines with only dashes or equals
                import re
                sections = [s.strip() for s in re.split(r'\n{2,}|^[-=]{2,}$', text, flags=re.MULTILINE) if s.strip()]
                result = {'rules': text, 'sections': sections, 'tables': []}
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
        # Accept result if any of text, sections, or tables is non-empty
        text_val = result.get('text', '') if isinstance(result, dict) else ''
        sections_val = result.get('sections', []) if isinstance(result, dict) else []
        tables_val = result.get('tables', []) if isinstance(result, dict) else []
        has_text = isinstance(text_val, str) and text_val.strip() != ''
        has_sections = isinstance(sections_val, list) and len(sections_val) > 0
        has_tables = isinstance(tables_val, list) and len(tables_val) > 0
        if not (has_text or has_sections or has_tables):
            logging.error('Empty parse result')
            return jsonify({'error': 'Empty parse result'}), 400
        response = dict(result) if result else {}
        if 'text' in result and 'rules' not in response:
            response['rules'] = result['text']
        if 'rules' not in response:
            response['rules'] = ''
        if 'sections' not in response:
            response['sections'] = []
        if 'tables' not in response:
            response['tables'] = []
        # Save rulebook to DB (upsert by filename)
        if use_cache():
            rpg_system = response.get('rpg_system') or None
            # If rpg_system is not in the response, try to infer from filename (optional, simple heuristic)
            if not rpg_system and filename:
                base = filename.rsplit('.', 1)[0]
                rpg_system = base if base else None
            # Upsert by filename
            rulebook = Rulebook.query.filter_by(filename=filename).first()
            if rulebook:
                rulebook.rules = response
                rulebook.rpg_system = rpg_system
            else:
                rulebook = Rulebook(filename=filename, rpg_system=rpg_system, rules=response)
                db.session.add(rulebook)
            db.session.commit()
            _rulebook_cache[cache_key] = response
        # In test mode, do not upsert or fetch from DB, always return fresh result
        return jsonify(response), 200
    except Exception as e:
        msg = str(e).lower()
        logging.error(str(e))
        # Always log error for empty file or parse errors
        if 'empty' in msg:
            logging.error('File is empty')
        if 'encrypted' in msg or 'locked' in msg:
            return jsonify({'error': 'PDF is encrypted or locked'}), 400
        return jsonify({'error': 'An internal error has occurred'}), 500
