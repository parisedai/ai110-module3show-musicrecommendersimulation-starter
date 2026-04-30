"""
Reliability Evaluator for Music Recommender System.

Provides confidence scoring, bias detection, edge case testing, and logging.
This is the core AI feature: demonstrating reliability and explainability.
"""

import logging
from typing import List, Dict, Tuple, Set
from collections import Counter
import json
from datetime import datetime


class ReliabilityLogger:
    """Track system decisions and errors for transparency."""

    def __init__(self, log_file: str = "logs/recommender_log.jsonl"):
        self.log_file = log_file
        self.entries = []
        
        # Ensure logs directory exists
        import os
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log_event(self, event_type: str, details: Dict) -> None:
        """Log an event with timestamp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            **details
        }
        self.entries.append(entry)
        
        # Write to file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_summary(self) -> Dict:
        """Return summary of logged events."""
        types = Counter(e["type"] for e in self.entries)
        return {
            "total_events": len(self.entries),
            "event_types": dict(types),
            "last_event": self.entries[-1] if self.entries else None
        }


class ConfidenceScorer:
    """
    Assign confidence scores to recommendations.
    
    Confidence reflects:
    - How well the song matches across dimensions (multi-match bonus)
    - How certain the preference is (perfect vs. partial match)
    - Distance from contradictions
    """

    @staticmethod
    def score_recommendation(user_prefs: Dict, song: Dict, base_score: float) -> Tuple[float, str]:
        """
        Return (confidence_0_to_1, reasoning).
        
        Confidence factors:
        - Perfect matches on multiple dimensions boost confidence
        - Contradictory preferences (e.g., high energy + sad) lower confidence
        - Extreme scores (very high or very low) are treated as more confident
        """
        confidence = 0.5  # Start neutral
        reasons = []

        # Count exact matches
        matches = 0
        if "genre" in user_prefs and song["genre"].lower() == str(user_prefs["genre"]).lower():
            matches += 1
        if "mood" in user_prefs and song["mood"].lower() == str(user_prefs["mood"]).lower():
            matches += 1
        
        # Multi-match bonus
        if matches >= 2:
            confidence = min(0.95, confidence + 0.30)
            reasons.append("multiple attribute matches")
        elif matches == 1:
            confidence += 0.15
            reasons.append("single attribute match")
        
        # Check for contradictions (high energy + sad, low valence)
        if "energy" in user_prefs and "valence" in user_prefs:
            user_energy = float(user_prefs["energy"])
            user_valence = float(user_prefs["valence"])
            contradiction_check = user_energy > 0.7 and user_valence < 0.4
            
            if contradiction_check:
                contradiction_song = song["energy"] > 0.7 and song["valence"] < 0.4
                if contradiction_song:
                    confidence += 0.10
                    reasons.append("matches contradictory preference")
                else:
                    confidence -= 0.15
                    reasons.append("contradictory user preference detected")
        
        # Normalize to [0, 1]
        confidence = max(0.0, min(1.0, confidence))
        
        reasoning = "; ".join(reasons) if reasons else "neutral match"
        return confidence, reasoning

    @staticmethod
    def format_confidence(confidence: float) -> str:
        """Return human-readable confidence label."""
        if confidence >= 0.85:
            return "🟢 High (≥0.85)"
        elif confidence >= 0.65:
            return "🟡 Medium (0.65-0.85)"
        else:
            return "🔴 Low (<0.65)"


class BiasDetector:
    """Detect potential biases in recommendations."""

    @staticmethod
    def analyze_recommendations(recommendations: List[Dict]) -> Dict:
        """
        Analyze a set of recommendations for bias patterns.
        
        Returns metrics on genre/mood distribution, overrepresentation, etc.
        """
        genres = [r["genre"] for r in recommendations]
        moods = [r["mood"] for r in recommendations]
        
        genre_counts = Counter(genres)
        mood_counts = Counter(moods)
        
        # Check for overrepresentation (e.g., >50% of one genre)
        total = len(recommendations)
        dominant_genre = genre_counts.most_common(1)[0] if genre_counts else None
        dominant_genre_pct = (dominant_genre[1] / total * 100) if dominant_genre else 0
        
        dominant_mood = mood_counts.most_common(1)[0] if mood_counts else None
        dominant_mood_pct = (dominant_mood[1] / total * 100) if dominant_mood else 0
        
        is_biased = dominant_genre_pct > 60 or dominant_mood_pct > 60
        
        return {
            "genre_distribution": dict(genre_counts),
            "mood_distribution": dict(mood_counts),
            "dominant_genre": dominant_genre[0] if dominant_genre else None,
            "dominant_genre_pct": round(dominant_genre_pct, 1),
            "dominant_mood": dominant_mood[0] if dominant_mood else None,
            "dominant_mood_pct": round(dominant_mood_pct, 1),
            "potential_bias_detected": is_biased,
            "message": f"⚠️  Bias Alert: {dominant_genre[0]} is {dominant_genre_pct:.0f}% of recommendations" if is_biased else "✅ Balanced recommendations across genres/moods"
        }


class EdgeCaseDetector:
    """Detect and handle edge cases in user preferences."""

    @staticmethod
    def detect_edge_cases(user_prefs: Dict) -> List[str]:
        """
        Identify potentially contradictory or unusual preferences.
        
        Edge cases:
        - High energy + sad mood
        - Very low danceability + high energy
        - Extreme preferences (0.0 or 1.0)
        """
        warnings = []
        
        # Check energy-mood contradiction
        if "energy" in user_prefs and "mood" in user_prefs:
            energy = float(user_prefs["energy"])
            mood = str(user_prefs["mood"]).lower()
            
            if energy > 0.75 and mood in ["sad", "melancholic", "intense"]:
                warnings.append("⚠️  Unusual: High energy + sad/intense mood (will favor upbeat sad songs)")
            elif energy < 0.3 and mood in ["euphoric", "joyful"]:
                warnings.append("⚠️  Unusual: Low energy + euphoric mood (will favor calm happy songs)")
        
        # Check danceability-energy mismatch
        if "danceability" in user_prefs and "energy" in user_prefs:
            dance = float(user_prefs["danceability"])
            energy = float(user_prefs["energy"])
            
            if dance > 0.8 and energy < 0.4:
                warnings.append("⚠️  Unusual: High danceability + low energy (rare combination)")
        
        # Extreme values
        for key in ["energy", "valence", "danceability"]:
            if key in user_prefs:
                val = float(user_prefs[key])
                if val <= 0.1 or val >= 0.95:
                    warnings.append(f"ℹ️  Extreme {key} preference ({val:.2f}) - may limit recommendations")
        
        return warnings


class RecommendationEvaluator:
    """
    Full evaluation pipeline: scoring, bias detection, edge cases.
    """

    def __init__(self):
        self.logger = ReliabilityLogger()

    def evaluate_recommendation_batch(
        self,
        user_prefs: Dict,
        recommendations: List[Tuple[Dict, float, str]],
        song_catalog: List[Dict]
    ) -> Dict:
        """
        Comprehensive evaluation of a recommendation batch.
        
        Returns:
        - Recommendations with confidence scores
        - Bias metrics
        - Edge case warnings
        - Overall system health
        """
        # Extract song data
        rec_songs = [r[0] for r in recommendations]
        
        # Edge case detection
        edge_cases = EdgeCaseDetector.detect_edge_cases(user_prefs)
        
        # Bias analysis
        bias_report = BiasDetector.analyze_recommendations(rec_songs)
        
        # Confidence scores
        rec_with_confidence = []
        for song, score, explanation in recommendations:
            confidence, conf_reasoning = ConfidenceScorer.score_recommendation(user_prefs, song, score)
            rec_with_confidence.append({
                "song": song,
                "score": score,
                "explanation": explanation,
                "confidence": confidence,
                "confidence_label": ConfidenceScorer.format_confidence(confidence),
                "confidence_reasoning": conf_reasoning
            })
        
        # Log the evaluation
        self.logger.log_event("recommendation_evaluation", {
            "recommendations_count": len(rec_with_confidence),
            "avg_confidence": round(sum(r["confidence"] for r in rec_with_confidence) / len(rec_with_confidence), 3) if rec_with_confidence else 0,
            "edge_cases_detected": len(edge_cases),
            "bias_detected": bias_report["potential_bias_detected"]
        })
        
        return {
            "recommendations": rec_with_confidence,
            "edge_cases": edge_cases,
            "bias_report": bias_report,
            "evaluation_timestamp": datetime.now().isoformat(),
            "system_health": self._compute_system_health(rec_with_confidence, edge_cases, bias_report)
        }

    @staticmethod
    def _compute_system_health(recommendations: List[Dict], edge_cases: List[str], bias_report: Dict) -> Dict:
        """Rate overall system health (0-100)."""
        health_score = 100
        issues = []
        
        # Penalize for low average confidence
        if recommendations:
            avg_conf = sum(r["confidence"] for r in recommendations) / len(recommendations)
            if avg_conf < 0.5:
                health_score -= 20
                issues.append("Low average confidence (<0.5)")
        
        # Penalize for edge cases
        if edge_cases:
            health_score -= min(15, len(edge_cases) * 5)
            issues.append(f"{len(edge_cases)} edge cases detected")
        
        # Penalize for bias
        if bias_report["potential_bias_detected"]:
            health_score -= 15
            issues.append(f"Bias detected: {bias_report['message']}")
        
        return {
            "score": max(0, health_score),
            "status": "🟢 Healthy" if health_score >= 80 else "🟡 Fair" if health_score >= 60 else "🔴 Poor",
            "issues": issues
        }
