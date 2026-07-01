import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import MODEL_NAME


class LyricsVectorSearch:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.songs = []
        self.embeddings = None
        self.index = None

    def load_documents(self, songs: list[dict]) -> None:
        self.songs = songs

    def process_documents(self) -> None:
        if not self.songs:
            raise ValueError("No songs loaded.")

        lyrics = [song["lyrics"] for song in self.songs]

        embeddings = self.model.encode(lyrics)
        self.embeddings = np.array(embeddings).astype("float32")

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

    def search(self, query: str, num_results: int = 3) -> list[dict]:
        if self.index is None:
            raise ValueError("The FAISS index has not been created yet.")

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, num_results)

        results = []

        for distance, index in zip(distances[0], indices[0]):
            song = self.songs[index]

            results.append({
                "title": song["title"],
                "filename": song["filename"],
                "score": float(distance),
                "lyrics_preview": song["lyrics"][:250]
            })

        return results