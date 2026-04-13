# 🎵 Music Recommender Simulation

## Project Summary

This music recommender simulation demonstrates how content-based filtering works by matching user preferences to song attributes. The system uses a weighted scoring algorithm that considers genre, mood, energy level, and acousticness to recommend songs from a curated catalog. Users can specify their favorite genre, preferred mood, target energy level, and whether they like acoustic music. The recommender then scores each song based on how well it matches these preferences and returns the top recommendations with explanations.

The project explores the challenges of algorithmic bias, transparency in AI recommendations, and how simple rules can create effective personalized experiences. It serves as an educational tool to understand how real-world music platforms like Spotify make suggestions.

---

## How The System Works

### Features Used
Each `Song` object uses these attributes from the CSV data:
- **Genre**: Categorical (pop, lofi, rock, electronic, etc.)
- **Mood**: Categorical (happy, chill, intense, energetic, etc.)  
- **Energy**: Numerical (0.0-1.0 scale, higher = more energetic)
- **Acousticness**: Numerical (0.0-1.0 scale, higher = more acoustic)

### User Profile
The `UserProfile` stores:
- Favorite genre (string)
- Favorite mood (string)
- Target energy level (float 0.0-1.0)
- Acoustic preference (boolean)

### Scoring Algorithm
The recommender computes a score for each song using:
1. **Genre Match**: +5.0 points for exact genre match
2. **Mood Match**: +3.0 points for exact mood match  
3. **Energy Proximity**: Up to +2.0 points based on how close song energy is to user target (closer = higher score)
4. **Acoustic Preference**: +1.0 point bonus if user likes acoustic and song has high acousticness (>0.5)

Songs are sorted by total score descending, and top K recommendations are returned with explanations.

### Recommendation Process
1. Load all songs from CSV into Song objects
2. Convert user preferences to UserProfile
3. Score every song against the profile
4. Sort by score and return top results with reasoning

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Diverse User Profile Testing
I tested the recommender with 5 different user profiles to evaluate its behavior across various tastes:

**High-Energy Pop Fan** (pop/happy/0.9 energy/no acoustic):
- Top recommendations: Pop songs with high energy (Sunrise City, Gym Hero)
- Results felt accurate - system correctly prioritized genre and energy matches

**Chill Lofi Listener** (lofi/chill/0.3 energy/acoustic):
- Top recommendations: All lofi tracks with low energy and acoustic elements
- Perfect matches for chill/acoustic preferences, showing the system handles low-energy profiles well

**Intense Rock Lover** (rock/intense/0.95 energy/no acoustic):
- Top: Storm Runner (exact rock match), then high-energy alternatives
- System correctly found the one rock song, then fell back to other intense/high-energy tracks

**Electronic Dance Enthusiast** (electronic/energetic/0.85 energy/no acoustic):
- Top: Electric Dreams (perfect match), then high-energy songs from other genres
- Demonstrated good energy matching when exact genre wasn't available

**Classical Music Aficionado** (classical/peaceful/0.25 energy/acoustic):
- Top: Classical Serenity (exact match), then ambient/acoustic alternatives
- Showed good fallback to similar peaceful/acoustic genres

### Weight Sensitivity Experiment
I temporarily doubled the genre weight from 5.0 to 10.0 points:
- Result: Genre matches dominated rankings even more, with "Storm Runner" jumping to #1 for the rock profile despite lower energy match
- This confirmed that genre weighting creates strong bias toward categorical preferences

### Feature Removal Test
I commented out the acoustic preference logic:
- Result: Rankings shifted slightly, with some acoustic-heavy songs losing their bonus
- Showed that the acoustic feature meaningfully impacts recommendations for certain user types

---

## Limitations and Risks

### Dataset Limitations
- **Small Catalog**: Only 20 songs limits diversity and discovery potential
- **Genre Bias**: Dataset over-represents pop/lofi/electronic genres, under-represents others
- **Synthetic Data**: All songs are artificially created, not real music data

### Algorithm Limitations  
- **Categorical Matching**: Exact string matches only - "indie pop" doesn't match "pop" perfectly
- **Feature Ignorance**: Ignores tempo_bpm, danceability, valence features that could improve matching
- **No Collaborative Filtering**: Purely content-based, doesn't learn from user behavior patterns
- **Static Weights**: Fixed scoring weights don't adapt to individual user preferences

### Bias Risks
- **Filter Bubbles**: Users only get recommendations within their stated preferences, limiting discovery
- **Majority Genre Bias**: Pop songs dominate recommendations due to dataset composition
- **Energy Stereotypes**: System assumes certain genres always have certain energy levels
- **Acoustic Assumptions**: Binary acoustic preference doesn't capture nuanced user tastes

### Real-World Risks
- **Over-Reliance on Self-Reported Preferences**: Users might not accurately describe their tastes
- **Lack of Context**: No consideration of time of day, activity, or mood changes
- **Cold Start Problem**: New users with unique tastes get poor recommendations

---

## Reflection

### What I Learned About AI Recommendations
Building this recommender opened my eyes to how much human judgment goes into "intelligent" systems. Every scoring weight, feature selection, and matching rule reflects subjective decisions about what makes music "good" or "similar." This mirrors real-world AI systems where engineers' assumptions about user behavior become embedded in the algorithms.

The experiments revealed that simple rules can create surprisingly effective recommendations, but they also create predictable biases. For example, the genre weight dominance showed how one design choice can create filter bubbles that limit user discovery. This made me appreciate why platforms like Spotify combine multiple recommendation approaches.

### AI Tools in Development
Copilot Chat was invaluable for brainstorming scoring algorithms and explaining technical concepts. It helped me understand the difference between collaborative vs. content-based filtering, and suggested diverse test profiles I might not have considered. However, I had to verify and adjust its suggestions - it initially proposed overly complex scoring formulas that didn't align with the project's educational goals.

### Biggest Surprises
The most surprising insight was how well the simple energy proximity scoring worked. I expected users would need exact matches, but the continuous energy scoring created natural-feeling recommendations even across different genres. This showed me that small algorithmic improvements can have outsized impacts on user experience.

### Future Extensions I'd Try
If I continued this project, I'd implement:
1. **Multi-feature scoring** incorporating tempo and danceability
2. **User feedback learning** to adjust weights based on actual preferences  
3. **Hybrid recommendations** combining content-based with simple collaborative filtering
4. **Context awareness** considering time of day or activity for recommendations

This project demonstrated that even basic AI systems require careful design thinking about fairness, transparency, and user experience - lessons that apply far beyond music recommendations.

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

