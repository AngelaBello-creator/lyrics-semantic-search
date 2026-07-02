from app.loader import load_lyrics_from_folder
from app.vector_search import LyricsVectorSearch


songs = load_lyrics_from_folder("data")

search_engine = LyricsVectorSearch()
search_engine.load_documents(songs)
search_engine.create_embeddings()
search_engine.build_index()

results = search_engine.search("songs about jealousy and obsession", num_results=3)

for result in results:
    print(result["title"], "-", result["artist"], "| score:", result["score"])
    print(result["lyrics_preview"])
    print("-" * 80)