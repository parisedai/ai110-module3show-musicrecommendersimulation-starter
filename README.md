# VibeBridge: Interactive Music Recommender with Reliability Evaluation

**Status:** Working. See the demo section below for the walkthrough video.

> **Base Project:** Music Recommender Simulation (Module 3)  
> **What I added:** reliability checks for confidence, bias, edge cases, and logging.

---

## 📋 Project Summary

This is a music recommender I built from my Module 3 project. It recommends songs from a local catalog and checks its own output so the results are easier to trust.

### Original Goal (Module 3)
Build a content-based music recommender that scores songs against user preferences and explains each recommendation.

### What I added in Module 5
I extended the recommender with a few checks so it can explain what it is doing and catch obvious problems:
- ✅ Confidence scoring (0–1, with reasoning)
- ✅ Bias detection (detects genre/mood overrepresentation)
- ✅ Edge case warnings (flags contradictory preferences)
- ✅ Structured logging (audit trail for every recommendation)
- ✅ Guardrails (prevents harmful outputs)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INPUT                                 │
│         (Taste Profile: genre, mood, energy, etc.)              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              EDGE CASE DETECTOR                                  │
│     (Flags contradictory preferences BEFORE recommending)        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         CONTENT-BASED RECOMMENDATION ENGINE                      │
│  (Score each song: genre match, mood match, feature distance)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│          CONFIDENCE SCORER                                       │
│   (Rate match strength: multi-dimension bonus, contradiction    │
│    penalty, extreme value handling)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            BIAS DETECTOR                                         │
│    (Analyze genre/mood distribution in top-K results)            │
│    (Alert if >60% from single genre/mood)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            RELIABILITY LOGGER                                    │
│     (Record all decisions in logs/recommender_log.jsonl)         │
│     (Enable audit trail + debugging)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────────┐
          │    EVALUATION REPORT             │
          │  (Recommendations + Confidence   │
          │   + Bias Metrics + Health Score) │
          └──────────────────────────────────┘
```

---

## 🎯 Key AI Features

### 1. **Confidence Scoring** (Reliability Testing)
- Rates recommendation match strength on 0–1 scale
- **Multi-dimension bonus:** Extra confidence if multiple attributes match
- **Contradiction detection:** Reduces confidence for paradoxical preferences
- **Reasoning explanation:** "🟢 High (≥0.85): multiple attribute matches"

**Example:**
```
Input: User likes pop + happy mood + high energy
Song: Upbeat Pop (pop genre, happy mood, 0.85 energy)
Confidence: 0.90 (🟢 High) - "multiple attribute matches"
```

### 2. **Bias Detection** (Fairness & Diversity)
- Analyzes top-K results for genre/mood overrepresentation
- Alert if >60% from single category
- Returns distribution metrics for transparency

**Example:**
```
Top 5 results: 4 pop songs, 1 rock song
Bias report: ⚠️ Pop is 80% of recommendations
Message: Bias Alert: pop is 80% of results
→ User might want to adjust preferences or get more diverse results
```

### 3. **Edge Case Detection** (Preference Validation)
- Flags contradictory preferences (e.g., high energy + sad mood)
- Warns on extreme values (0.0–0.1 or 0.95–1.0)
- Explains unusual combinations that might or might not be intentional

**Example:**
```
Input: Energy 0.85, Valence 0.2, Mood "sad"
Warning: ⚠️ Unusual: High energy + sad/intense mood
         (will favor upbeat sad songs like intense rock ballads)
```

### 4. **Structured Logging & Guardrails** (Transparency)
- All evaluations logged to `logs/recommender_log.jsonl` (JSON Lines format)
- Includes timestamp, event type, recommendation count, confidence scores, bias flags
- Enables auditing and debugging

**Example log entry:**
```json
{
  "timestamp": "2026-04-29T14:32:15.123456",
  "type": "recommendation_evaluation",
  "recommendations_count": 5,
  "avg_confidence": 0.75,
  "edge_cases_detected": 1,
  "bias_detected": false
}
```

---

## 🚀 Setup Instructions

### Requirements
- Python 3.8 or higher
- pandas, pytest, streamlit (see `requirements.txt`)

### Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify the setup:**
```bash
pytest tests/test_evaluator.py -v
```

### Running the System

**Option 1: Full demo (both basic + evaluated modes)**
```bash
python -m src.main
```

**Option 2: Just basic recommendations (original mode)**
```bash
python -m src.main --mode basic
```

**Option 3: Full evaluation with metrics**
```bash
python -m src.main --mode evaluated
```

**Option 4: Interactive mode (enter your preferences)**
```bash
python -m src.main --mode interactive
```

---

## 💡 Sample Interactions

### Example 1: Balanced Profile

**Input:**
```
Profile: High-Energy Pop Lover
Preferences: pop, happy, energy=0.85, valence=0.8, danceability=0.8, acoustic=False
```

**Sample Output:**
```
🎵 TOP 5 RECOMMENDATIONS:

1. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Energy: 0.82 | Valence: 0.84 | Danceability: 0.79
   Score: 6.58 | Confidence: 🟢 High (≥0.85)
   Why: genre match (+2.0); mood match (+1.0); 
        energy closeness (+1.97); danceability closeness (+0.79)
   Confidence reasoning: multiple attribute matches

📊 System Health: 🟢 Healthy (95/100)
📈 Bias Analysis: genre distribution {'pop': 3, 'indie-pop': 1, 'afrobeats': 1} → Balanced

✅ No edge cases detected in this preference profile.
```

### Example 2: Edge Case Profile (Intentional Contradiction)

**Input:**
```
Profile: Upbeat Sadness
Preferences: pop, sad, energy=0.85, valence=0.25, danceability=0.65, acoustic=False
```

**Sample Output:**
```
⚠️ EDGE CASES DETECTED:
  ⚠️  Unusual: High energy + sad/intense mood 
     (will favor upbeat sad songs)

🎵 TOP 5 RECOMMENDATIONS:
   [Songs with high energy but low valence/sad mood]

📊 System Health: 🟡 Fair (72/100)
   - Warning: 1 edge case detected

📈 Bias Analysis: ⚠️ Bias Alert: pop is 75% of results
```

### Example 3: Chill Lofi Preference

**Input:**
```
Profile: Chill Lofi Vibe
Preferences: lofi, chill, energy=0.35, acoustic=True
```

**Sample Output:**
```
🎵 TOP 5 RECOMMENDATIONS:

1. Library Rain - Paper Lanterns
   Genre: lofi | Mood: chill
   Energy: 0.35 | Acousticness: 0.86
   Score: 4.82 | Confidence: 🟢 High
   Why: genre match (+2.0); mood match (+1.0); acoustic match (+0.75)

🏥 System Health: 🟢 Healthy (90/100)

✅ No edge cases detected
✅ Balanced recommendations across genres/moods
```

---

## 🔍 Testing & Reliability

### Test Summary

✅ **17/17 tests pass:**
- Confidence scoring logic ✓
- Bias detection accuracy ✓
- Edge case detection ✓
- Logging functionality ✓
- Recommendation consistency ✓
- Integration pipeline ✓

### Run Tests

```bash
pytest tests/ -v
```

### What The Tests Verify

1. **Confidence Scoring:** Multi-match bonus, contradiction detection, extreme values
2. **Bias Detection:** Genre overrepresentation >60%, balanced distributions, reporting
3. **Edge Cases:** Contradictions (high energy + sad), extreme values (0.0, 1.0)
4. **Logging:** Events recorded, summaries computed, audit trail preserved
5. **Integration:** Full pipeline from preferences → recommendations → evaluation

---

## 📊 Design Decisions & Trade-offs

| Decision | Why | Trade-off |
|----------|-----|-----------|
| Rule-based scoring vs. embeddings | No external APIs; fully transparent; meets 4-hour deadline | Less sophisticated than ML models |
| Confidence scoring on 0–1 scale | Normalized scores easy to interpret | May not reflect true uncertainty |
| Bias threshold at 60% | Flags obvious dominance; not too strict | Some legitimate cases might alert |
| JSON logging | Human + machine readable; easy to audit | More disk I/O than binary formats |
| No external API dependencies; lightweight local Python packages only | Simpler deployment; fits constraints | Can't use robust ML libraries |

---

## 🎓 What We Learned

### Working With Restrictions
- **No LLM API access** forced us to use rule-based logic → made the system more transparent
- **4-hour deadline** meant we prioritized testing + guardrails over feature quantity
- **Small catalog (18 songs)** taught us that data quality matters as much as algorithm

### Transparency Over Complexity
- Confidence scores + bias reports prove reliability better than just rankings
- Logging makes debugging and accountability much easier
- Edge case detection prevents surprising recommendations

### The Reality of Bias
- Bias emerges from data (limited genres), not just algorithm
- Acknowledging contradictions is better than silently downranking them
- Evaluation is as important as generation

---

## 📹 Demo Video

**[Loom Recording](#)** - *Link will be added after recording*

Demo shows:
- ✅ System running with 3 different user profiles
- ✅ Confidence scores and bias detection in action
- ✅ Edge case warning system catching contradictions
- ✅ Logging & reliability metrics summary

**Duration:** ~5 minutes  
**Content:** End-to-end system run with outputs + interpretation

---

## 📁 Project Structure

```
.
├── README.md               ← This file
├── model_card.md           ← Reflections on bias, misuse, AI collaboration
├── requirements.txt        ← Python dependencies
├── data/
│   └── songs.csv          ← Song catalog (18 songs)
├── src/
│   ├── __init__.py
│   ├── main.py            ← CLI entry point (original + new modes)
│   ├── recommender.py     ← Core scoring algorithm
│   ├── evaluator.py       ← Confidence, bias, edge case detection, logging
│   └── interactive_system.py  ← Interactive mode + full pipeline
├── tests/
│   ├── test_recommender.py    ← Original tests
│   └── test_evaluator.py      ← New reliability tests (6 test classes, 20+ tests)
├── logs/
│   └── recommender_log.jsonl  ← Generated during runtime (audit trail)
├── assets/
│   └── SYSTEM_ARCHITECTURE.md  ← Architecture documentation (diagram + flow)
```

---

## 🛡️ Responsible Design & Ethics

### Limitations We Acknowledge
1. **Small dataset:** Only 18 songs; misses many genres and languages
2. **Genre bias:** Algorithm can collapse toward dominant genres
3. **No learning:** Single fixed profile per recommendation; doesn't adapt
4. **Acoustic oversimplification:** Binary threshold (≥0.6 vs. <0.6) misses nuance

### How We Mitigate Risk
- ✅ **Full transparency:** Every recommendation includes score, confidence, reasoning
- ✅ **Bias alerts:** System warns when >60% from one genre
- ✅ **Edge case detection:** Flags contradictions before recommending
- ✅ **Logging:** Audit trail for every recommendation enables accountability

### Ethical Principles
- No hidden ranking manipulation
- Explainability by default
- User preferences respected (not overridden by business logic)
- Guardrails prevent edge case failures

---

## 🔮 Future Enhancements

- **Diversity constraint:** Reshuffle top-5 if >2 from same artist
- **Feedback loop:** Rate recommendations → adjust weights
- **Expanded catalog:** >100 songs with better genre/language balance
- **Temporal analysis:** Seasonal music trends
- **Benchmark comparison:** vs. random baseline + popularity

---

## 👤 Author Notes

This project evolved from a simple content-based recommender into a system demonstrating **both capability and responsibility**. The key insight: evaluating your own recommendations (confidence, bias, edge cases) matters as much as generating them.

**For potential employers:** This code shows I can:
- Build modular, testable systems
- Add reliability/guardrails to AI pipelines
- Balance transparency with functionality
- Work within constraints (time, compute, API access)
- Document clearly with examples

---

## 📝 License

Educational use. See original Module 3 project for details.

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