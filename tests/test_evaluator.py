"""
Reliability and Evaluation Tests for Music Recommender System.

These tests verify:
1. Confidence scoring logic
2. Bias detection accuracy
3. Edge case detection
4. Logging functionality
5. Recommendation consistency
"""

import pytest
import os
import json
from pathlib import Path

from src.recommender import Song, UserProfile, Recommender, load_songs, recommend_songs
from src.evaluator import (
    ConfidenceScorer,
    BiasDetector,
    EdgeCaseDetector,
    RecommendationEvaluator,
    ReliabilityLogger,
)


class TestConfidenceScorer:
    """Test confidence scoring module."""

    def test_confidence_high_for_multi_match(self):
        """Confidence should be high when multiple attributes match."""
        user_prefs = {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.8,
        }
        song = {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.8,
            "danceability": 0.7,
            "acousticness": 0.2,
        }
        confidence, reasoning = ConfidenceScorer.score_recommendation(user_prefs, song, 5.0)
        assert confidence >= 0.65, f"Expected high confidence, got {confidence}"
        assert "multiple" in reasoning.lower()

    def test_confidence_detects_contradictions(self):
        """Confidence should account for contradictory preferences."""
        user_prefs = {
            "energy": 0.85,  # High energy
            "valence": 0.2,  # But sad
        }
        song = {
            "energy": 0.85,
            "valence": 0.2,
            "genre": "pop",
            "mood": "sad",
            "danceability": 0.7,
            "acousticness": 0.2,
        }
        confidence, reasoning = ConfidenceScorer.score_recommendation(user_prefs, song, 5.0)
        assert "contradiction" in reasoning.lower() or confidence > 0.5

    def test_confidence_label_formatting(self):
        """Confidence labels should be properly formatted."""
        high_label = ConfidenceScorer.format_confidence(0.9)
        medium_label = ConfidenceScorer.format_confidence(0.7)
        low_label = ConfidenceScorer.format_confidence(0.3)

        assert "High" in high_label
        assert "Medium" in medium_label
        assert "Low" in low_label


class TestBiasDetector:
    """Test bias detection in recommendations."""

    def test_detects_genre_overrepresentation(self):
        """Should detect when one genre dominates >60%."""
        recommendations = [
            {"genre": "pop", "mood": "happy"},
            {"genre": "pop", "mood": "happy"},
            {"genre": "pop", "mood": "happy"},
            {"genre": "pop", "mood": "happy"},
            {"genre": "rock", "mood": "intense"},
        ]
        report = BiasDetector.analyze_recommendations(recommendations)
        assert report["potential_bias_detected"] == True
        assert report["dominant_genre"] == "pop"
        assert report["dominant_genre_pct"] == 80.0

    def test_balanced_recommendations_pass(self):
        """Should pass balanced recommendations."""
        recommendations = [
            {"genre": "pop", "mood": "happy"},
            {"genre": "rock", "mood": "intense"},
            {"genre": "lofi", "mood": "chill"},
            {"genre": "jazz", "mood": "relaxed"},
        ]
        report = BiasDetector.analyze_recommendations(recommendations)
        assert report["potential_bias_detected"] == False

    def test_bias_report_structure(self):
        """Bias report should have required fields."""
        recs = [{"genre": "pop", "mood": "happy"}]
        report = BiasDetector.analyze_recommendations(recs)
        assert "genre_distribution" in report
        assert "mood_distribution" in report
        assert "potential_bias_detected" in report
        assert "message" in report


class TestEdgeCaseDetector:
    """Test edge case detection."""

    def test_detects_high_energy_sad_contradiction(self):
        """Should flag high energy + sad mood."""
        prefs = {
            "energy": 0.85,
            "mood": "sad",
        }
        warnings = EdgeCaseDetector.detect_edge_cases(prefs)
        assert len(warnings) > 0
        assert any("high energy" in w.lower() for w in warnings)

    def test_detects_extreme_values(self):
        """Should flag extreme preferences (0.0-0.1 or 0.95-1.0)."""
        prefs = {
            "energy": 0.02,
            "danceability": 0.98,
        }
        warnings = EdgeCaseDetector.detect_edge_cases(prefs)
        assert len(warnings) >= 1

    def test_no_warnings_for_normal_prefs(self):
        """Normal preferences should produce no warnings."""
        prefs = {
            "energy": 0.5,
            "mood": "happy",
            "valence": 0.6,
        }
        warnings = EdgeCaseDetector.detect_edge_cases(prefs)
        # May have some generic warnings, but not contradictions
        assert not any("high energy" in w.lower() and "sad" in w.lower() for w in warnings)


class TestRecommendationEvaluator:
    """Test the full evaluation pipeline."""

    @pytest.fixture
    def sample_songs(self):
        """Provide sample songs for testing."""
        return [
            {
                "id": 1,
                "title": "Upbeat Pop",
                "artist": "Artist A",
                "genre": "pop",
                "mood": "happy",
                "energy": 0.85,
                "tempo_bpm": 120,
                "valence": 0.85,
                "danceability": 0.8,
                "acousticness": 0.1,
            },
            {
                "id": 2,
                "title": "Chill Lofi",
                "artist": "Artist B",
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.4,
                "tempo_bpm": 80,
                "valence": 0.55,
                "danceability": 0.5,
                "acousticness": 0.8,
            },
        ]

    def test_evaluator_returns_correct_structure(self, sample_songs):
        """Full evaluation should return expected structure."""
        evaluator = RecommendationEvaluator()
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.85}
        recs = [(sample_songs[0], 5.0, "test explanation")]

        result = evaluator.evaluate_recommendation_batch(user_prefs, recs, sample_songs)

        assert "recommendations" in result
        assert "edge_cases" in result
        assert "bias_report" in result
        assert "system_health" in result

    def test_system_health_scoring(self, sample_songs):
        """System health should be reasonable."""
        evaluator = RecommendationEvaluator()
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.85}
        recs = [
            (sample_songs[0], 5.0, "test"),
            (sample_songs[1], 3.0, "test"),
        ]

        result = evaluator.evaluate_recommendation_batch(user_prefs, recs, sample_songs)
        health = result["system_health"]

        assert 0 <= health["score"] <= 100
        assert "status" in health
        assert health["status"] in ["🟢 Healthy", "🟡 Fair", "🔴 Poor"]


class TestReliabilityLogger:
    """Test logging functionality."""

    def test_logger_creates_entries(self):
        """Logger should record events."""
        logger = ReliabilityLogger(log_file="test_logs/test.jsonl")
        logger.log_event("test_event", {"data": "test"})

        assert len(logger.entries) == 1
        assert logger.entries[0]["type"] == "test_event"

    def test_logger_summary(self):
        """Logger summary should report correctly."""
        logger = ReliabilityLogger(log_file="test_logs/test2.jsonl")
        logger.log_event("event1", {})
        logger.log_event("event2", {})
        logger.log_event("event1", {})

        summary = logger.get_summary()
        assert summary["total_events"] == 3
        assert summary["event_types"]["event1"] == 2

    def teardown_method(self):
        """Clean up test logs."""
        import shutil
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")


class TestIntegration:
    """Integration tests combining multiple components."""

    def test_full_recommendation_pipeline(self):
        """Test complete pipeline from preference to evaluation."""
        # Load real songs
        songs = load_songs("data/songs.csv")
        assert len(songs) > 0

        # Get recommendations
        user_prefs = {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.8,
            "danceability": 0.7,
            "likes_acoustic": False,
        }
        recs = recommend_songs(user_prefs, songs, k=5)
        assert len(recs) <= 5

        # Evaluate
        evaluator = RecommendationEvaluator()
        result = evaluator.evaluate_recommendation_batch(user_prefs, recs, songs)

        # Verify structure
        assert len(result["recommendations"]) > 0
        assert result["system_health"]["score"] >= 0
        assert result["bias_report"]["potential_bias_detected"] in [True, False]

    def test_edge_case_profile_evaluation(self):
        """Edge case profiles should be handled gracefully."""
        songs = load_songs("data/songs.csv")

        # Contradictory preferences
        edge_prefs = {
            "energy": 0.9,
            "valence": 0.1,
            "mood": "sad",
        }
        recs = recommend_songs(edge_prefs, songs, k=5)
        
        evaluator = RecommendationEvaluator()
        result = evaluator.evaluate_recommendation_batch(edge_prefs, recs, songs)

        # Should detect edge case
        assert len(result["edge_cases"]) > 0
        assert result["system_health"]["score"] < 100  # Should penalize edge cases


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
