from app.loader import load_lyrics_from_folder

songs = load_lyrics_from_folder("data")

print(f"Loaded {len(songs)} songs\n")

for song in songs:
    print(song)
    print("-" * 80)