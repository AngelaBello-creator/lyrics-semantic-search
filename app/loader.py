from pathlib import Path

from app.models import Song


def load_lyrics_from_folder(folder_path: str) -> list[Song]:
    folder = Path(folder_path)
    songs = []

    for file_path in folder.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        song = parse_song_file(content)
        songs.append(song)

    return songs


def parse_song_file(content: str) -> Song:
    lines = content.splitlines()

    metadata = {}
    lyrics_lines = []
    reading_metadata = True

    for line in lines:
        line = line.strip()

        if reading_metadata and ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip().lower()] = value.strip()
        else:
            reading_metadata = False
            if line:
                lyrics_lines.append(line)

    return Song(
        title=metadata.get("title", "Unknown Title"),
        artist=metadata.get("artist", "Unknown Artist"),
        album=metadata.get("album", "Unknown Album"),
        year=int(metadata.get("year", 0)),
        genre=metadata.get("genre", "Unknown Genre"),
        language=metadata.get("language", "Unknown Language"),
        lyrics="\n".join(lyrics_lines)
    )