from app.models import Song
from app.vector_search import LyricsVectorSearch


def test_semantic_search_returns_results():
    songs = [
        Song(
            title="Sad Song",
            artist="Test Artist",
            album="Test Album",
            year=2024,
            genre="Pop",
            language="English",
            lyrics="I miss you every night and I feel lonely without you.",
        ),
        Song(
            title="Party Song",
            artist="Test Artist",
            album="Test Album",
            year=2024,
            genre="Dance",
            language="English",
            lyrics="We dance all night under bright lights and loud music.",
        ),
    ]

    search_engine = LyricsVectorSearch()
    search_engine.load_documents(songs)
    search_engine.create_embeddings()
    search_engine.build_index()

    results = search_engine.search("a song about dancing", num_results=1)

    assert len(results) == 1
    assert results[0].title == "Party Song"