from app.loader import parse_song_file
from app.models import Song


def test_parse_song_file_returns_song():
    content = """Title: Test Song
Artist: Test Artist
Album: Test Album
Year: 2024
Genre: Pop
Language: English

This is the first lyric line.
This is the second lyric line.
"""

    song = parse_song_file(content)

    assert isinstance(song, Song)
    assert song.title == "Test Song"
    assert song.artist == "Test Artist"
    assert song.album == "Test Album"
    assert song.year == 2024
    assert song.genre == "Pop"
    assert song.language == "English"
    assert "first lyric line" in song.lyrics


def test_parse_song_file_uses_default_values():
    content = """Title: Minimal Song

Only one lyric line.
"""

    song = parse_song_file(content)

    assert song.title == "Minimal Song"
    assert song.artist == "Unknown Artist"
    assert song.album == "Unknown Album"
    assert song.year == 0
    assert song.genre == "Unknown Genre"
    assert song.language == "Unknown Language"
    assert song.lyrics == "Only one lyric line."