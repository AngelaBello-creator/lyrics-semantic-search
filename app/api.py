from fastapi import FastAPI, HTTPException, Query

from app.config import DATA_FOLDER, TOP_K
from app.loader import load_lyrics_from_folder
from app.schemas import SearchResponse, SongResponse
from app.vector_search import LyricsVectorSearch

app = FastAPI(
    title="Lyrics Semantic Search API",
    description="Semantic search engine for song lyrics using Sentence Transformers and FAISS.",
    version="1.0.0",
)

search_engine = LyricsVectorSearch()


@app.on_event("startup")
def startup_event():
    songs = load_lyrics_from_folder(DATA_FOLDER)

    if not songs:
        raise RuntimeError("No songs found in the data folder.")

    search_engine.load_documents(songs)
    search_engine.create_embeddings()
    search_engine.build_index()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/songs", response_model=list[SongResponse])
def get_songs():
    return [
        SongResponse(
            title=song.title,
            artist=song.artist,
            album=song.album,
            year=song.year,
            genre=song.genre,
            language=song.language,
        )
        for song in search_engine.songs
    ]


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., description="Semantic search query"),
    limit: int = Query(TOP_K, ge=1, le=10),
):
    try:
        results = search_engine.search(q, limit)

        return SearchResponse(
            query=q,
            limit=limit,
            results=results,
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error