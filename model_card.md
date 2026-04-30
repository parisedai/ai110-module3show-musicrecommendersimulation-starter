# 🎧 Model Card: Music Recommender System

**Note:** This is an extended version of the Module 3 Music Recommender. The original system recommended songs from a CSV catalog. This version adds **reliability evaluation**: confidence scoring, bias detection, edge case handling, and structured logging.

---

## Part 1: Original System (Module 3 Base)

## 1. Model Name

**VibeBridge 2.0** – An interactive music recommender with reliability guardrails.

**Base Project:** Music Recommender Simulation (Module 3)

---

## 2. Intended Use

This system recommends songs from a local catalog based on user taste profiles. It combines:
- **Content-based scoring** (genre, mood, energy, valence, danceability, acousticness)
- **Transparency features** (explanations for each recommendation)
- **Reliability evaluation** (confidence scores, bias detection, edge case warnings)

**Design Goal:** Demonstrate how to build a recommender with guardrails, not just accuracy.

---

## 3. How the System Works

### Recommendation Engine (Original)
- Scores each song against user preferences
- Genre and mood matches get fixed bonuses
- Numeric features (energy, valence, danceability) use distance-based scoring
- Acoustic preference adds conditional bonus

### Reliability Layer (New)
- **Confidence Scoring:** Evaluates match strength across multiple dimensions
- **Bias Detection:** Identifies when one genre/mood dominates >60% of results
- **Edge Case Detection:** Flags contradictory preferences (e.g., high energy + sad mood)
- **Logging & Guardrails:** Records all system decisions for transparency

---

## 4. Data

**Catalog:** 18 songs in `data/songs.csv`

**Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, afrobeats, post-punk, classical, rnb, folk, edm, hip hop, indie

**Limitations:** Small dataset, English-language bias, limited representation of non-Western music

---

## 5. Model Strengths

✅ **Transparent:** Every recommendation includes human-readable explanations  
✅ **Evaluable:** Confidence scores and bias metrics show why results matter  
✅ **Robust:** Edge case detection prevents contradictory recommendations  
✅ **Reproducible:** Scoring is deterministic and rule-based  
✅ **No API dependency:** Runs fully offline with no external calls

---

## Part 2: System Reliability & Evaluation

## 6. Limitations and Potential Biases

### Data Bias
- **Small catalog** (18 songs) cannot represent the full music landscape
- **Genre underrepresentation:** Missing classical forms, regional music, non-English tracks
- **Mood stereotyping:** Mood labels are subjective; same song may be interpreted differently
- **Artist & language bias:** Catalog leans toward English-language pop/mainstream artists

### Algorithm Bias
- **Genre dominance:** If genre weight is high, results can collapse to one genre even when energy/mood fit better elsewhere
- **Population homogeneity:** Assumes single stable profile per user; ignores context-dependent taste
- **Acoustic vs. studio bias:** Acoustic preference is binary (≥0.6 vs. <0.6), missing nuance

### System Limitations
- No temporal learning (can't adapt from user feedback)
- No collaborative filtering (ignores what similar users like)
- No lyrics, cultural context, or social signals
- Contradictory preferences acknowledged but not well-resolved

---

## 7. Testing & Reliability Summary

### Test Coverage
- **Unit tests:** Confidence scoring, bias detection, edge case logic ✅
- **Integration tests:** Full pipeline from preference → recommendation → evaluation ✅
- **Edge case tests:** Contradictory preferences, extreme values, genre homogeneity ✅

### Reliability Metrics
- **✅ 15 of 15 new reliability tests passed**
- **✅ 2 of 2 original recommender tests passed**
- **TOTAL: 17 of 17 tests pass** ✓
- **Confidence scoring:** Averages 0.70-0.75 for normal profiles, flags contradictions correctly
- **Bias detection:** Successfully identifies >60% genre dominance in skewed catalogs
- **Edge case detection:** Catches high-energy + sad combinations, extreme preference values

### Known Issues & Trade-offs
- ⚠️ **Limited recommendations for rare genres:** Small catalog means fewer alternatives for niche preferences
- ⚠️ **Confidence scoring may be overly conservative:** Penalizes contradictions even when they're intentional
- ⚠️ **No ranking diversity constraint:** Top-5 results may all be from same artist/subgenre

---

## 8. Preventing Misuse & Responsible Design

### How Could This System Be Misused?

1. **Filter Bubble Risk:** Using high genre weights to lock users into narrow musical styles
   - **Mitigation:** Bias detection alerts when >60% of results from single genre
   
2. **Representation Loss:** Using simplified acoustic/mood labels that don't represent diverse musical traditions
   - **Mitigation:** Edge case warnings when preferences seem contradictory invite user reflection
   
3. **Over-reliance on Scores:** Treating recommendation scores as objective "taste" rather than preference model
   - **Mitigation:** System always shows confidence scores and reasoning, never just rank

### Design Safeguards

- 🛡️ **Transparency:** Every recommendation includes score, confidence, AND explanation
- 🛡️ **Guardrails:** Edge case detection warns before recommending contradictory matches
- 🛡️ **Logging:** All evaluations logged (in `logs/recommender_log.jsonl`) for audit trail
- 🛡️ **No external influence:** Pure content-based; can't be manipulated by paid placement

---

## Part 3: AI Collaboration & Development

## 9. How I Collaborated with AI During This Project

### Instance 1: AI Suggestion That Helped ✅

**What I asked:** "How should I structure reliability testing for a recommendation system?"

**AI's suggestion:** "Use three parallel evaluation paths: (1) confidence scoring for match certainty, (2) bias detection for unfair dominance, (3) edge case detection for contradictions. Then combine into a system health score."

**Why it worked:** This gave me a clean architecture to build on. I implemented each module independently, then composed them. The three-path design made the system modular and testable.

**My contribution:** I refined the confidence scoring algorithm to account for multi-dimensional matches and adjusted the health scoring weights based on testing.

---

### Instance 2: AI Suggestion That Was Flawed ❌

**What I asked:** "Should I use an embedding model to compute song similarity?"

**AI suggested:** "Yes—use sentence-transformers to embed song metadata and compute cosine similarity. This would improve matching beyond just rule-based scoring."

**Why it was flawed:** 
1. Adds external dependency (defeats the "no API" goal for this timeline)
2. Requires additional libraries and setup time (I had ~4 hours total)
3. Embeddings are a black-box; contradicts the explainability goal
4. Overkill for a 18-song catalog

**What I did instead:** Stuck with rule-based scoring but added structured confidence annotations. Gave me both speed and transparency.

**Lesson learned:** AI suggestions are valuable starting points, but context matters. Constraints (time, compute, explainability requirements) should guide whether to adopt a suggestion.

---

## 10. What Surprised Me During Testing

1. **Contradictions aren't always wrong:** The "High Energy + Sad" profile actually makes sense (think aggressive punk or intense rock ballads). The system now acknowledges this rather than penalizing it.

2. **Bias emerges from data, not just logic:** Even with balanced weights, a small catalog naturally creates genre concentration. This forced me to separate "bias in data" from "bias in algorithm."

3. **Confidence scoring is hard to calibrate:** My initial confidence thresholds were too aggressive. After testing, I found that 0.65 is a better neutral point than 0.5.

---

## 11. Original Model Card Content (Module 3)

*(Preserved from original submission for reference)*

### Strengths (Original)
- The system is transparent: every recommendation includes reasons.
- It works well for focused profiles like high-energy pop or chill lofi.
- Distance-based scoring for numeric features captures vibe similarity better than simple threshold checks.
- Because rules are explicit, it is easy to debug and tune.

### Evaluation (Original)
I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and Edge Case: High Energy + Sad.  
I reviewed whether top-5 outputs matched expected vibe and inspected reason strings for each ranking.  
I also ran a weight-shift experiment (decrease genre weight, increase energy weight).

**Key finding:** Ranking order is highly sensitive to weight changes, even though the same songs are scored.

### Personal Reflection (Original)

The biggest learning moment was seeing that recommendation quality depends as much on ranking design as on data quality. Even simple weighted scoring can feel personalized, but it is easy to accidentally encode narrow assumptions.

This project changed how I think about music apps: what seems like neutral personalization is often the result of many subjective choices in features, weights, and data coverage.

---

## 12. Evolution: From Module 3 to Final Project

| Aspect | Module 3 | Module 5 (Final) |
|--------|----------|-----------------|
| **Purpose** | Learn content-based recommendation | Demonstrate reliable AI with guardrails |
| **Output** | Rankings + score explanations | Rankings + confidence + bias analysis + edge case warnings |
| **Testing** | Manual profile inspection | Automated test suite + reliability metrics |
| **Logging** | Console output only | Persistent JSON logging for audit trail |
| **User interaction** | CLI with predefined profiles | CLI + interactive mode + evaluation reports |
| **AI feature** | Content-based scoring | Reliability evaluation (confidence + bias detection + edge cases) |

---

## 13. Future Work

- Add diversity constraints (if >2 songs from same artist in top-5, reshuffle)
- Implement user feedback loop (rate recommendations → retrain weights)
- Extend catalog to >100 songs with better genre/language balance
- Add time-series analysis (seasonal music preference shifts)
- Compare against simple baseline (random + popularity)

