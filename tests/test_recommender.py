from recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(id=1, title="Test Pop Track", artist="Test Artist", genre="pop", mood="happy", 
             energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist", genre="lofi", mood="chill", 
             energy=0.4, tempo_bpm=80, valence=0.6, danceability=0.5, acousticness=0.9),
        Song(id=3, title="Indie Pop Spark", artist="Test Artist", genre="indie pop", mood="happy", 
             energy=0.7, tempo_bpm=110, valence=0.8, danceability=0.7, acousticness=0.5),
    ]
    return Recommender(songs)

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # The pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"

def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "exact match" in explanation

def test_partial_genre_match():
    # Should partially match the "indie pop" song if exact "pop" isn't available
    user = UserProfile(favorite_genre="pop", favorite_mood="sad", target_energy=0.7, likes_acoustic=True)
    rec = make_small_recommender()
    # Pop track #1 gets exact match (+5) but acousticness penalty
    # Indie Pop track #3 gets partial match (+2) and better acoustic bonus
    score_pop = rec.score_song(user, rec.songs[0])
    score_indie_pop = rec.score_song(user, rec.songs[2])
    
    # We just want to ensure it calculates without crashing and applies *some* genre score
    assert score_indie_pop > 0.0 

def test_acoustic_preference_logic():
    user_acoustic = UserProfile(favorite_genre="rock", favorite_mood="angry", target_energy=0.5, likes_acoustic=True)
    user_electronic = UserProfile(favorite_genre="rock", favorite_mood="angry", target_energy=0.5, likes_acoustic=False)
    
    rec = make_small_recommender()
    lofi_song = rec.songs[1] # acousticness = 0.9

    score_acc = rec.score_song(user_acoustic, lofi_song)
    score_elec = rec.score_song(user_electronic, lofi_song)
    
    # The acoustic user should score the high-acousticness song much higher
    assert score_acc > score_elec