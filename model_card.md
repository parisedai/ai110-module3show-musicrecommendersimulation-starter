# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeBridge 1.0

---

## 2. Intended Use

This model recommends 3 to 5 songs from a small local catalog based on a user taste profile. It is designed for classroom exploration of recommendation concepts, not for production music platforms.

It assumes users can be represented by a few stable preferences (genre, mood, energy, valence, danceability, acoustic preference). That assumption is useful for teaching but too simple for real listeners.

---

## 3. How the Model Works

The model compares each song to user preferences, gives points for matches, then sorts songs by total points.

- Genre match gets a strong bonus.
- Mood match gets a smaller bonus.
- Numeric features (energy, valence, danceability) use closeness scoring, so values near the target get more points.
- Acoustic preference adds a small bonus when the song texture matches the profile.

Compared to the starter version, the final model now loads typed data from CSV, computes weighted scores with explanations, supports optional weight experiments, and ranks songs by descending score.

---

## 4. Data

The catalog currently contains 18 songs in `data/songs.csv`.

Represented genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, afrobeats, post-punk, classical, rnb, folk, edm, hip hop, and indie.

I expanded the starter data by adding 8 songs to increase diversity of moods and styles. Even with this expansion, the dataset is still small and misses many music traditions, languages, and subgenres.

---

## 5. Strengths

- The system is transparent: every recommendation includes reasons.
- It works well for focused profiles like high-energy pop or chill lofi.
- Distance-based scoring for numeric features captures vibe similarity better than simple threshold checks.
- Because rules are explicit, it is easy to debug and tune.

---

## 6. Limitations and Bias

The model can still create filter bubbles. A high genre weight can dominate other features, so songs from one genre can repeatedly appear even when mood or emotional intent is different.

The model ignores sequence behavior (skips, replays, session context) and social signals that real systems use. It also ignores lyrics, language, and cultural context, which can be major drivers of listener preference.

The scoring assumes linear preference distance and one user profile at a time. This can under-represent users with contradictory, evolving, or multi-context taste.

---

## 7. Evaluation

I tested four profiles:

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Edge Case: High Energy + Sad

I reviewed whether top-5 outputs matched expected vibe and inspected reason strings for each ranking. I also ran a weight-shift experiment (decrease genre weight, increase energy weight) to see how sensitive results are to design choices.

What surprised me most was how quickly ranking order changes when one weight changes, even though the same songs are being scored.

---

## 8. Future Work

- Add diversity constraints so top results are not all from one genre/artist.
- Add temporal behavior signals (skip rate, repeat plays, recent sessions).
- Use pairwise learning or feedback loops to tune weights from user behavior instead of fixed constants.
- Improve explanations with tradeoffs (for example, "great energy match but weaker mood match").

---

## 9. Personal Reflection

The biggest learning moment was seeing that recommendation quality depends as much on ranking design as on data quality. Even simple weighted scoring can feel personalized, but it is easy to accidentally encode narrow assumptions.

AI tools helped with brainstorming profiles and bias checks, but I still needed to verify logic and interpret outputs manually. This project changed how I think about music apps: what seems like neutral personalization is often the result of many subjective choices in features, weights, and data coverage.
