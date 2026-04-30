# Loom Video Demo Checklist (5-7 minutes)

## What to Show ✅

### Section 1: Intro & System Overview (1 min)
- [ ] Show the terminal window with the project directory visible
- [ ] Say: "This is VibeBridge 2.0, a music recommender with reliability evaluation."
- [ ] Say: "It extends my Module 3 project by adding confidence scoring, bias detection, and edge case warnings."
- [ ] Point to `README.md` and briefly mention the 3 AI features

---

### Section 2: Run Basic Mode (1.5 mins)
Show the original recommender still works:

```bash
python3 -m src.main --mode basic
```

- [ ] Briefly scroll through output showing genre/mood/score combinations
- [ ] Point out it gives explanations for each recommendation
- [ ] Say: "The original recommender is here — it scores songs based on user preferences."

---

### Section 3: Run Full Evaluation Mode (2-2.5 mins)
**THIS IS THE CORE DEMO - The AI Feature**

```bash
python3 -m src.main --mode evaluated
```

Show at least **3 different profiles:**

#### Profile 1: "High-Energy Pop Lover" (Balanced)
- [ ] Explain the input preferences
- [ ] Highlight the **Confidence Score** output (show 🟢 High / 🟡 Medium labels)
- [ ] Point to one song's explanation: "Why it scored this way"
- [ ] Show **System Health: 🟢 Healthy (100/100)**
- [ ] Explain what the health score means

#### Profile 2: "Upbeat Sadness" (Edge Case)
- [ ] Show the **⚠️ EDGE CASES DETECTED** section
- [ ] Explain: "This is contradictory — high energy + sad mood is unusual"
- [ ] Point out **System Health dropped to 🟡 Fair** because of the contradiction
- [ ] Demonstrate how the system WARNS the user instead of silently breaking

#### Profile 3: One More Profile (Your Choice)
- [ ] Show the **📈 BIAS ANALYSIS** output
- [ ] Explain the genre distribution
- [ ] Point to the message: "✅ Balanced recommendations" or "⚠️ Bias Alert"

---

### Section 4: Show Reliability Features (1 min)
Briefly showcase each evaluation component:

```bash
ls -la logs/
cat logs/recommender_log.jsonl
```

- [ ] Show that a log file was created
- [ ] Read one JSON line from the log: Explain timestamp, recommendations_count, confidence metrics
- [ ] Say: "Every recommendation is logged for accountability and debugging"

---

### Section 5: Run Tests (30 seconds)
Prove the system is reliable:

```bash
python3 -m pytest tests/ -v --tb=short
```

- [ ] Show the test results
- [ ] Say: "17 out of 17 tests pass — confidence scoring, bias detection, edge cases, all validated"

---

### Section 6: Quick File Tour (30 seconds)
Show the modular structure:

```bash
tree src/
cat assets/SYSTEM_ARCHITECTURE.md | head -50
```

- [ ] Point to `evaluator.py` as the core reliability module
- [ ] Mention they can read the architecture in `/assets/SYSTEM_ARCHITECTURE.md`

---

### Section 7: Wrap-Up & Reflection (30 seconds)
- [ ] Show the README.md in GitHub (https://github.com/parisedai/ai110-module3show-musicrecommendersimulation-starter)
- [ ] Point to model_card.md with reflections
- [ ] Final quote: "This project shows how to build AI systems that are not just accurate, but reliable and explainable."

---

## Key Points to Emphasize During Recording

✅ **End-to-end system run** - Show inputs → recommendations → evaluation → output  
✅ **AI feature behavior** - Confidence scoring, bias detection, edge case warnings all active  
✅ **Reliability/guardrail behavior** - Logs, health scoring, edge case detection working  
✅ **Clear outputs** - Every output includes explanations, confidence labels, reasoning  

## Technical Setup Before Recording

1. Open terminal, cd to project directory
2. Make sure venv is activated (or use `python3` directly)
3. Make sure tests pass (`pytest tests/ -v`)
4. Clear the terminal so recording starts fresh and clean
5. Zoom in on terminal (Cmd + to increase font size) so viewers can read output

## Recording Tips

- **Use Loom's standard video recording** (no need for screen+webcam)
- **Narrate as you go** - explain what you're showing, not just the output
- **Go slow** - let viewers read the confidence scores and explanations
- **Pause between sections** - gives viewers time to absorb information
- **Aim for 5-7 minutes** - you have room to be clear without rambling

## After Recording

1. Save the Loom video URL
2. Add it to README.md in the "Demo Video" section: `[Loom Recording](YOUR_LOOM_URL_HERE)`
3. Commit & push:
   ```bash
   git add README.md
   git commit -m "docs: Add Loom demo video link"
   git push origin main
   ```

---

## Backup: If You Can't Use Loom

If Loom has issues, here's a terminal-based recording alternative:

```bash
# Record terminal output to GIF using asciinema
brew install asciinema
asciinema rec demo.cast
# Then convert to GIF and upload

# OR just take screenshots of the important outputs and add them to README.md
```

---

**Good luck with the video! You've got this. 🎬**
