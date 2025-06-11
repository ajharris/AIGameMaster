import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Simple chunking utility
def chunk_text(text, chunk_size=200):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Simple embedding utility (TF-IDF)
def embed_texts(texts):
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(texts).toarray()
    return embeddings, vectorizer

# Simple in-memory vector store
class SimpleVectorStore:
    def __init__(self):
        self.texts = []
        self.embeddings = None
        self.nn = None
    def add(self, texts, embeddings):
        self.texts.extend(texts)
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        self.nn = NearestNeighbors(n_neighbors=1, metric='cosine').fit(self.embeddings)
    def search(self, query_embedding, top_k=1):
        distances, indices = self.nn.kneighbors(query_embedding, n_neighbors=top_k)
        return [(self.texts[i], distances[0][j]) for j, i in enumerate(indices[0])]
