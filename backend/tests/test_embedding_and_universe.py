import os
import uuid
import pytest
from backend.utils_embedding import chunk_text, embed_texts, SimpleVectorStore
from backend.models import Rulebook, Universe, UserUniverseShare
from backend.app import db

# Use the correct path to the PDF in the project root
env_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
PDF_PATH = os.path.join(env_root, "Erick Wujcik - Ninjas and Superspies-Palladium Books (1994).pdf")

# 🧪 Test: PDF Parsing and Chunking
def test_pdf_parsing_and_chunking():
    import PyPDF2
    with open(PDF_PATH, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    chunks = chunk_text(text, chunk_size=100)
    assert isinstance(chunks, list)
    assert all(isinstance(c, str) for c in chunks)
    assert len(chunks) > 1

# 🧠 Test: Embedding Generation
def test_embedding_generation():
    texts = ["Ninja rules", "Spy gadgets", "Martial arts moves"]
    embeddings, vectorizer = embed_texts(texts)
    assert embeddings.shape[0] == len(texts)
    assert embeddings.shape[1] > 0

# 📦 Test: Store Embeddings in Vector Database
def test_store_embeddings_and_search():
    texts = ["Ninja rules", "Spy gadgets", "Martial arts moves"]
    embeddings, _ = embed_texts(texts)
    store = SimpleVectorStore()
    store.add(texts, embeddings)
    query = [embeddings[0]]
    results = store.search(query, top_k=1)
    assert results[0][0] == texts[0]
    assert results[0][1] >= 0

# 🧬 Test: Link Rules to RPG System ID
def test_link_rules_to_rpg_system(app):
    with app.app_context():
        rulebook = Rulebook(filename="test.pdf", rpg_system="Ninjas & Superspies", rules={"rules": "Test rules"})
        db.session.add(rulebook)
        db.session.commit()
        found = Rulebook.query.filter_by(rpg_system="Ninjas & Superspies").first()
        assert found is not None
        assert found.rpg_system == "Ninjas & Superspies"

# 👥 Test: Universe Sharing Between Users
def test_universe_sharing_between_users(app):
    with app.app_context():
        universe = Universe(name="Test World", owner_id="user1")
        db.session.add(universe)
        db.session.commit()
        share = UserUniverseShare(universe_id=universe.id, user_id="user2")
        db.session.add(share)
        db.session.commit()
        # Owner and shared user should both have access
        owner_access = Universe.query.filter_by(id=universe.id, owner_id="user1").first()
        shared_access = UserUniverseShare.query.filter_by(universe_id=universe.id, user_id="user2").first()
        assert owner_access is not None
        assert shared_access is not None
