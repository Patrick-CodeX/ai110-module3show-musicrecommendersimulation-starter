from typing import List, Dict, Tuple, Optional
import csv
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        scored_songs = []
        for song in self.songs:
            score = 0.0
            if song.genre.lower() == user.favorite_genre.lower():
                score += 5.0
            if song.mood.lower() == user.favorite_mood.lower():
                score += 3.0

        # Energy proximity (lower difference = higher score)
        energy_diff = abs(song.energy - user.target_energy)
        score += (1.0 - energy_diff) * 2
        
        # Acoustic preference
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 1.0

        scored_songs.append((song, score))

    # Sort by score descending and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:k]]
    

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"it matches your favorite genre ({user.favorite_genre})")
        if abs(song.energy - user.target_energy) < 0.2:
            reasons.append("the energy level matches your preference")
        
        return f"Recommended because {' and '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(Song(
                id=int(row['id']),
                title=row['title'],
                artist=row['artist'],
                genre=row['genre'],
                mood=row['mood'],
                energy=float(row['energy']),
                tempo_bpm=float(row['tempo_bpm']),
                valence=float(row['valence']),
                danceability=float(row['danceability']),
                acousticness=float(row['acousticness'])
            ))
    return songs

def recommend_songs(user_prefs: Dict, songs_data: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    # 1. Convert Dicts to Objects
    songs = [Song(**s) for s in songs_data] # This assumes keys match exactly
    user = UserProfile(**user_prefs)
    
    # 2. Use the Recommender class
    rec_engine = Recommender(songs)
    top_songs = rec_engine.recommend(user, k)
    
    # 3. Format as requested: (song_dict, score, explanation)
    results = []
    for s in top_songs:
        explanation = rec_engine.explain_recommendation(user, s)
        # Note: You'd need to calculate the score again or return it from recommend()
        results.append((s.__dict__, 0.0, explanation)) 
    return results
