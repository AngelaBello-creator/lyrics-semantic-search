import logging

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import MODEL_NAME
from app.models import Song
from app.schemas import SearchResult

logger = logging.getLogger(__name__)


class LyricsVectorSearch:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.songs: list[Song] = []
        self.embeddings = None
        self.index = None

    def load_documents(self, songs: list[Song]) -> None:
        self.songs = songs

    def create_embeddings(self) -> None:
        if not self.songs:
            raise ValueError("No songs loaded.")

        lyrics = [song.lyrics for song in self.songs]

        embeddings = self.model.encode(lyrics)
        self.embeddings = np.array(embeddings).astype("float32")

        logger.info("Created embeddings with shape %s", self.embeddings.shape)

    def build_index(self) -> None:
        if self.embeddings is None:
            raise ValueError("Embeddings have not been created.")

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

        logger.info("FAISS index created with %s vectors.", self.index.ntotal)

    def search(self, query: str, num_results: int = 3) -> list[SearchResult]:
        if self.index is None:
            raise ValueError("FAISS index has not been created.")

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, num_results)

        results = []

        for distance, index in zip(distances[0], indices[0]):
            song = self.songs[index]

            results.append(
                SearchResult(
                    title=song.title,
                    artist=song.artist,
                    album=song.album,
                    year=song.year,
                    genre=song.genre,
                    language=song.language,
                    score=float(distance),
                    lyrics_preview=song.lyrics[:250],
                )
            )

        return results