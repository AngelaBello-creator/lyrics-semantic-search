from fastapi import FastAPI, Query

from app.config import DATA_FOLDER, TOP_K
from app.loader import load_lyrics_from_folder
from app.vector_search import LyricsVectorSearch

app = FastAPI(
    title="Lyrics Semantic Search API",
    description="Semantic search engine for song lyrics using Sentence Transformers and FAISS.",
    version="1.0.0"
)

search_engine = LyricsVectorSearch()


@app.on_event("startup")
def startup_event():
    songs = load_lyrics_from_folder(DATA_FOLDER)
    search_engine.load_documents(songs)
    search_engine.process_documents()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/songs")
def get_songs():
    return {
        "total": len(search_engine.songs),
        "songs": [
            {
                "title": song["title"],
                "filename": song["filename"]
            }
            for song in search_engine.songs
        ]
    }


@app.get("/search")
def search(
    q: str = Query(..., description="Semantic search query"),
    limit: int = Query(TOP_K, ge=1, le=10)
):
    results = search_engine.search(q, limit)

    return {
        "query": q,
        "results": results
    }