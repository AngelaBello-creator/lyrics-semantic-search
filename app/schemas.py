from pydantic import BaseModel


class SongResponse(BaseModel):
    title: str
    artist: str
    album: str
    year: int
    genre: str
    language: str


class SearchResult(BaseModel):
    title: str
    artist: str
    album: str
    year: int
    genre: str
    language: str
    score: float
    lyrics_preview: str


class SearchResponse(BaseModel):
    query: str
    limit: int
    results: list[SearchResult]