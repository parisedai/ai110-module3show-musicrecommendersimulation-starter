# VibeBridge System Architecture

## High-Level Flow Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                     USER INPUT (Taste Profile)                     │
│            [Genre, Mood, Energy, Valence, Danceability]            │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│          VALIDATION LAYER: Edge Case Detector                      │
│    • Flags contradictory preferences (high energy + sad)           │
│    • Warns on extreme values (0.0-0.1 or 0.95-1.0)               │
│    • Checks for unusual combinations                              │
│                                                                    │
│  INPUT: User preferences → OUTPUT: List of warnings/notifications │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│          SCORING LAYER: Content-Based Recommendation              │
│  For each song in catalog:                                         │
│    • Genre match: +2.0                                            │
│    • Mood match: +1.0                                             │
│    • Energy closeness: (1 - |user - song|) × 2.0                 │
│    • Valence closeness: (1 - |user - song|) × 1.0                │
│    • Danceability closeness: (1 - |user - song|) × 1.0           │
│    • Acoustic preference: +0.75 if matches                        │
│  TOTAL: Sum of all applicable points                              │
│                                                                    │
│  INPUT: User prefs + Song catalog → OUTPUT: (song, score) pairs   │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│       CONFIDENCE LAYER: Confidence Scorer                          │
│  For each (song, score) pair:                                      │
│    1. Check multi-dimensional match:                              │
│       - 2+ matches → confidence += 0.30                           │
│       - 1 match → confidence += 0.15                              │
│    2. Detect contradictions:                                       │
│       - High energy + low valence match → confidence += 0.10      │
│       - else (mismatch) → confidence -= 0.15                      │
│    3. Normalize to [0.0, 1.0]                                     │
│                                                                    │
│  OUTPUT: Confidence score (0-1) + reasoning                       │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│          RANKING LAYER: Bias Detector                              │
│  1. Sort recommendations by score (descending)                     │
│  2. Take top-K (default K=5)                                       │
│  3. Analyze distribution:                                          │
│     - Top genre percentage?                                        │
│     - Top mood percentage?                                         │
│  4. Alert if any category > 60% (potential filter bubble)         │
│                                                                    │
│  OUTPUT: Ranked list + bias metrics                               │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│         LOGGING LAYER: Reliability Logger                          │
│  Record to logs/recommender_log.jsonl:                            │
│    - timestamp                                                     │
│    - event_type: "recommendation_evaluation"                      │
│    - recommendations_count                                         │
│    - avg_confidence                                               │
│    - edge_cases_detected                                          │
│    - bias_detected (true/false)                                   │
│                                                                    │
│  PURPOSE: Audit trail, debugging, compliance                      │
│                                                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│          OUTPUT LAYER: Evaluation Report                           │
│                                                                    │
│  For each recommendation:                                          │
│    - Song metadata (title, artist, genre, mood)                   │
│    - Audio features (energy, valence, danceability, etc.)         │
│    - Score & explanation                                          │
│    - Confidence label (🟢 High / 🟡 Medium / 🔴 Low)             │
│    - Confidence reasoning                                         │
│                                                                    │
│  System-level metrics:                                             │
│    - 🏥 System Health (0-100 score)                               │
│    - ⚠️  Edge case warnings (if any)                              │
│    - 📈 Bias analysis (genre/mood distribution)                   │
│    - 📋 Logging summary                                            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. **RECOMMENDER` (src/recommender.py)**
- **Purpose:** Core content-based scoring algorithm
- **Inputs:** User preferences dict, Song catalog list
- **Outputs:** List of (song, score, explanation) tuples
- **Responsibility:** Scoring logic only, no evaluation

### 2. **EVALUATOR** (src/evaluator.py)
- **ConfidenceScorer:** Rates match strength (0-1)
- **BiasDetector:** Analyzes genre/mood distribution
- **EdgeCaseDetector:** Flags contradictory preferences
- **RecommendationEvaluator:** Orchestrates all three + computes health score
- **ReliabilityLogger:** Records all events to JSON log file

### 3. **INTERACTIVE_SYSTEM** (src/interactive_system.py)
- **InteractiveRecommenderSystem:** Combines recommender + evaluator
- **Methods:**
  - `recommend_with_evaluation()`: Single recommendation batch
  - `print_evaluation_report()`: Pretty-print results
- **Modes:**
  - Demo mode: Predefined profiles
  - Interactive mode: User input

### 4. **MAIN** (src/main.py)
- **CLI entry point** with argument parsing
- **Modes:**
  - `--mode basic`: Original recommender only
  - `--mode evaluated`: Full evaluation pipeline
  - `--mode interactive`: User input mode
  - `--mode full` (default): Both basic + evaluated

---

## Data Flow Example

### Input: High-Energy Pop Lover

```json
{
  "genre": "pop",
  "mood": "happy",
  "energy": 0.85,
  "valence": 0.8,
  "danceability": 0.8,
  "likes_acoustic": false
}
```

### Step 1: Edge Case Detection
```
✅ No contradictions found (high energy + happy mood is coherent)
```

### Step 2: Scoring
```
Song: "Sunrise City" by Neon Echo
- Genre match: pop == pop → +2.0
- Mood match: happy == happy → +1.0
- Energy: |0.82 - 0.85| = 0.03 → (1 - 0.03) × 2.0 = 1.94
- Valence: |0.84 - 0.80| = 0.04 → (1 - 0.04) × 1.0 = 0.96
- Danceability: |0.79 - 0.80| = 0.01 → (1 - 0.01) × 1.0 = 0.99
- Acoustic: 0.18 < 0.6 → no match (user doesn't like acoustic) → +0.75
TOTAL SCORE: 2.0 + 1.0 + 1.94 + 0.96 + 0.99 + 0.75 = **7.64**
```

### Step 3: Confidence Scoring
```
Confidence baseline: 0.5
+ Multi-match bonus: Genre ✓ + Mood ✓ = 0.30 → 0.80
- Contradiction check: None detected
- Normalize: 0.80 (already in range)
CONFIDENCE: **0.80 (🟡 Medium)**
REASONING: "multiple attribute matches"
```

### Step 4: Bias Detection
```
Top 5 genres: pop (2), indie pop (1), afrobeats (1), hip hop (1)
Distribution: pop 40%, others 20% each
Threshold: >60%? NO
BIAS STATUS: ✅ Balanced
```

### Step 5: System Health
```
- Avg confidence: 0.70 ✓
- Edge cases: 0 ✓
- Bias detected: false ✓
HEALTH SCORE: **100/100 🟢 Healthy**
```

### Step 6: Logging
```json
{
  "timestamp": "2026-04-29T14:32:15.123456",
  "type": "recommendation_evaluation",
  "recommendations_count": 5,
  "avg_confidence": 0.70,
  "edge_cases_detected": 0,
  "bias_detected": false
}
```

### Final Output
```
Recommendation #1: Sunrise City - Neon Echo
Score: 7.64 | Confidence: 🟡 Medium (0.65-0.85)
Why: genre match (+2.0); mood match (+1.0); energy closeness (+1.94); 
     valence closeness (+0.96); danceability closeness (+0.99); acoustic (+0.75)
Confidence reasoning: multiple attribute matches
```

---

## Testing Architecture

```
tests/
├── test_recommender.py
│   ├── test_recommend_returns_songs_sorted_by_score()
│   └── test_explain_recommendation_returns_non_empty_string()
│
└── test_evaluator.py
    ├── TestConfidenceScorer
    │   ├── test_confidence_high_for_multi_match()
    │   ├── test_confidence_detects_contradictions()
    │   └── test_confidence_label_formatting()
    │
    ├── TestBiasDetector
    │   ├── test_detects_genre_overrepresentation()
    │   ├── test_balanced_recommendations_pass()
    │   └── test_bias_report_structure()
    │
    ├── TestEdgeCaseDetector
    │   ├── test_detects_high_energy_sad_contradiction()
    │   ├── test_detects_extreme_values()
    │   └── test_no_warnings_for_normal_prefs()
    │
    ├── TestRecommendationEvaluator
    │   ├── test_evaluator_returns_correct_structure()
    │   └── test_system_health_scoring()
    │
    ├── TestReliabilityLogger
    │   ├── test_logger_creates_entries()
    │   └── test_logger_summary()
    │
    └── TestIntegration
        ├── test_full_recommendation_pipeline()
        └── test_edge_case_profile_evaluation()
```

**Test Coverage:**
- ✅ 6 test classes
- ✅ 20+ individual test methods
- ✅ Unit tests for each component
- ✅ Integration tests for full pipeline
- ✅ Edge case validation
