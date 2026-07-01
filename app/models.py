from dataclasses import dataclass


@dataclass
class Song:
    title: str
    artist: str
    album: str
    year: int
    language: str
    lyrics: str