from typing import List, Dict, Tuple, Any
import csv
from dataclasses import dataclass

@dataclass
class Song:
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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> float:
        score = 0.0
        
        # 1. Exact vs. Partial Genre Match
        if song.genre.lower() == user.favorite_genre.lower():
            score += 5.0
        elif user.favorite_genre.lower() in song.genre.lower():
            score += 2.0  # E.g. "pop" is inside "indie pop"
            
        # 2. Mood Match
        if song.mood.lower() == user.favorite_mood.lower():
            score += 3.0

        # 3. Energy Proximity (Closer = Higher Score, up to 3 points)
        energy_diff = abs(song.energy - user.target_energy)
        score += max(0.0, (1.0 - energy_diff)) * 3.0

        # 4. Acousticness continuous scaling
        if user.likes_acoustic:
            # Reward high acousticness
            score += song.acousticness * 2.0
        else:
            # Reward low acousticness (more electronic/produced tracks)
            score += (1.0 - song.acousticness) * 2.0

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            score = self.score_song(user, song)
            scored_songs.append((song, score))

        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"it's an exact match for your favorite genre ({user.favorite_genre})")
        elif user.favorite_genre.lower() in song.genre.lower():
            reasons.append("it's similar to your favorite genre")
            
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"it fits your '{user.favorite_mood}' mood")
            
        if abs(song.energy - user.target_energy) <= 0.15:
            reasons.append("the energy level perfectly aligns with your preference")
            
        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append("it features the acoustic style you enjoy")
        elif not user.likes_acoustic and song.acousticness <= 0.4:
            reasons.append("it has the electronic/produced sound you prefer")
            
        if not reasons:
            return "it has a well-balanced profile that loosely aligns with your overall tastes"
            
        return f"Recommended because {', and '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Cast numeric columns properly
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict[str, Any], songs_data: List[Dict[str, Any]], k: int = 5) -> List[Tuple[Dict[str, Any], float, str]]:
    # Convert incoming data to internal classes
    if len(songs_data) > 0 and isinstance(songs_data[0], Song):
        songs = songs_data
    else:
        songs = [Song(**s) for s in songs_data]

    if isinstance(user_prefs, UserProfile):
        user = user_prefs
    else:
        user = UserProfile(
            favorite_genre=user_prefs.get("favorite_genre", user_prefs.get("genre", "")),
            favorite_mood=user_prefs.get("favorite_mood", user_prefs.get("mood", "")),
            target_energy=float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5))),
            likes_acoustic=bool(user_prefs.get("likes_acoustic", False)),
        )

    rec_engine = Recommender(songs)
    top_songs = rec_engine.recommend(user, k)

    results = []
    for s in top_songs:
        score = rec_engine.score_song(user, s)
        explanation = rec_engine.explain_recommendation(user, s)
        results.append((s.__dict__, score, explanation))
    return results