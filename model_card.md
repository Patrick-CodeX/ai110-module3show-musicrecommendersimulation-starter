# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
**VibeFinder 2.0**  

---

## 2. Intended Use  
This model suggests 3 to 5 songs from a small curated catalog based on a user's stated preferences for genre, mood, acousticness, and energy level. It is built strictly as a classroom exploration tool to demonstrate how heuristic scoring algorithms match data profiles to user preferences, rather than for commercial production.

---

## 3. How the Model Works  
The system uses a point-based scoring logic to rank songs:
- **Genre & Mood (Categorical):** It checks if the user's favorite genre and mood match the song's metadata. Exact matches grant a large point bonus. I also added a "partial match" feature so that if a user loves "pop", a song tagged "indie pop" still receives a slight bonus.
- **Energy & Acousticness (Continuous):** Instead of a simple true/false, the model measures the *distance* between a user's ideal energy level and the song's actual energy. The closer they are, the more points the song gets. If a user states they don't like acoustic music, it actively rewards tracks with highly produced, electronic sounds (low acousticness).
- **Ranking:** All points are added together, and the tracks with the highest scores are returned with an auto-generated sentence explaining *why* they won.

---

## 4. Data  
The data consists of a tiny mock catalog (`songs.csv`) containing 10 synthetic tracks. 
- The dataset heavily represents popular, accessible genres like Pop, Lofi, Synthwave, and Indie. 
- **Missing Elements:** Large swaths of musical taste are completely omitted. There is no classical, hip-hop, metal, or country music. Because the dataset is so small, a user looking for a specific niche will likely get completely unrelated recommendations purely because the system was forced to pick *something*.

---

## 5. Strengths  
- **Transparency:** The absolute biggest strength of this system is that it's highly interpretable. Because it uses hard-coded rules instead of deep learning, we can instantly generate an accurate explanation for why a song was chosen.
- **Continuous Logic:** By scaling points based on distance for attributes like "Energy," the system produces much softer, more realistic rankings rather than strict "pass/fail" cliffs.

---

## 6. Limitations and Bias 
- **Over-indexing on Stated Preferences:** It assumes users only ever want to listen to their absolute favorite genre and mood, which isn't how humans actually listen to music. 
- **Feature Ignorance:** Features like `tempo_bpm` and `danceability` exist in the CSV but are currently ignored by the scoring engine.
- **Categorical Bias:** If a genre is misspelled or arbitrarily named differently ("lofi" vs "lo-fi"), the system will cruelly punish the score, exposing a bias against non-standard tagging. 

---

## 7. Evaluation  
I checked the system by writing an automated test suite (`pytest`) simulating various user types:
- **Exact Matches:** Confirmed that a pop-loving user reliably gets Pop music.
- **Edge Cases:** Evaluated an "Acoustic vs. Electronic" test. I fed the same highly acoustic Lofi song to two users with identical tastes, except one liked acoustic and one didn't. Confirmed the system properly boosted and penalized the track respectively.

---

## 8. Future Work  
If I had more time, I would:
1. Include `tempo_bpm` and `danceability` in the logic, mapping them to specific "moods" (e.g., Happy -> High danceability).
2. Implement collaborative filtering (e.g., "Users who liked this also liked...").
3. Introduce a "discovery" randomness metric to occasionally serve a wild-card song outside the user's standard tastes to prevent recommendation loops.

---

## 9. Personal Reflection  
Building this simulation clarified just how many arbitrary choices go into "algorithmic" systems. I had to personally decide that an exact genre match was worth exactly 5 points, and a mood match was worth 3. This means my own human bias regarding what matters most in music is permanently baked into the math. It completely changes the way I think about apps like Spotify—their "smart" AI is ultimately built on thousands of human assumptions about how humans behave.