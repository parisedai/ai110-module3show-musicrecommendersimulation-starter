# 🎵 Music Recommender Simulation

## Project Summary

This project builds a CLI-first music recommender that scores songs from a CSV catalog against user taste profiles, then ranks the top matches with human-readable reasons. It simulates a content-based recommender (genre, mood, energy, valence, danceability, acousticness) and shows how small design choices in scoring weights can strongly change results.

In real platforms, recommendations typically combine:

- Collaborative filtering: learns from behavior patterns across many users (likes, skips, watch time, playlist adds).
- Content-based filtering: matches item attributes to user preferences (tempo, mood, genre, audio embeddings).

This simulation focuses on content-based logic for transparency and learning.

---

## How The System Works

### Data and Features

Each song uses:

- Categorical: genre, mood
- Numeric: energy, tempo_bpm, valence, danceability, acousticness

Each user profile stores target preferences for the same vibe dimensions:

- Preferred genre and mood
- Target energy / valence / danceability
- Acoustic preference
- Optional weight overrides for experiments

### Algorithm Recipe

Scoring rule for one song:

- Genre match: +2.0
- Mood match: +1.0
- Energy closeness: $\max(0, 1 - |song.energy - user.energy|) \times 2.0$
- Optional valence closeness: same distance-based style (default weight 1.0)
- Optional danceability closeness: same distance-based style (default weight 1.0)
- Acoustic preference match: +0.75

Ranking rule for many songs:

- Score every song independently
- Sort by score descending
- Return top $k$

Why both rules matter:

- Scoring decides quality per item.
- Ranking decides which few items survive when many songs are "good enough."

### Potential Bias (Known Early)

- If genre weight is too high, recommendations can collapse to one genre even when mood/energy fit better elsewhere.
- Small catalogs can create filter bubbles because there are not enough alternatives.

### Data Flow

```mermaid
flowchart LR
    A[User Preferences] --> B[Load songs.csv]
    B --> C[Score one song at a time]
    C --> D[Attach reasons to each score]
    D --> E[Sort all songs by score]
    E --> F[Top K recommendations]
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

---

## Evaluation Runs

Profiles tested in CLI:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Edge Case: High Energy + Sad

Experiment tested:

- Weight shift: lower genre influence and increase energy influence

How to capture evidence for submission:

- Run `python -m src.main`
- Take terminal screenshots for each profile section
- Add the screenshots under this README section

---

## Limitations and Risks

- The catalog is tiny (18 songs), so many recommendations repeat.
- The model cannot use listening history sequences (skips, repeat behavior).
- Lyrics, language, cultural context, and novelty are ignored.
- A fixed weighted sum may under-serve users with mixed or evolving tastes.

---

## Reflection

Building this made the scoring/ranking split very clear: a simple formula can feel surprisingly "smart" but still be brittle. I also learned that explanation strings are useful for debugging bias, because they reveal exactly why songs rise to the top.

AI tools were most helpful for quickly drafting and stress-testing profile ideas, but I still had to verify math and data assumptions manually. Small recommenders can create convincing outputs while still overfitting to narrow feature definitions, which is a useful reminder that transparency and evaluation matter even in toy systems.

### Evaluation Screenshots

#### Profile Runs (Part 1)
![CLI output - profile runs part 1](images/recommender-output-1.png)


#### Profile Runs (Part 2 + Experiment)
![CLI output - profile runs part 2](images/recommender-output-2.png)