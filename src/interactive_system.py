"""
Interactive Music Recommender System with Reliability Evaluation.

This is the main entry point that demonstrates:
1. The base recommender system
2. Confidence scoring
3. Bias detection
4. Edge case handling
5. Full logging and guardrails
"""

import sys
from typing import Dict, List, Tuple
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from recommender import load_songs, recommend_songs
    from evaluator import RecommendationEvaluator, EdgeCaseDetector, ConfidenceScorer
except ImportError:
    from .recommender import load_songs, recommend_songs
    from .evaluator import RecommendationEvaluator, EdgeCaseDetector, ConfidenceScorer


class InteractiveRecommenderSystem:
    """
    Interactive system that combines recommendation and evaluation.
    Demonstrates: reliability, transparency, and responsible AI practices.
    """

    def __init__(self, songs_path: str = "data/songs.csv"):
        self.songs = load_songs(songs_path)
        self.evaluator = RecommendationEvaluator()
        print(f"✅ System initialized. Loaded {len(self.songs)} songs.")

    def recommend_with_evaluation(self, user_prefs: Dict, k: int = 5) -> Dict:
        """
        Generate recommendations AND evaluate their reliability.
        Returns comprehensive report with confidence, bias, and edge cases.
        """
        # Get raw recommendations
        raw_recs = recommend_songs(user_prefs, self.songs, k=k)

        # Full evaluation
        evaluation = self.evaluator.evaluate_recommendation_batch(
            user_prefs,
            raw_recs,
            self.songs
        )

        return evaluation

    def print_evaluation_report(self, evaluation: Dict, profile_name: str = "User Profile") -> None:
        """Pretty-print the full evaluation report."""
        print(f"\n{'='*80}")
        print(f"📊 RECOMMENDATION REPORT: {profile_name}")
        print(f"{'='*80}")

        # System Health
        health = evaluation["system_health"]
        print(f"\n🏥 System Health: {health['status']} ({health['score']}/100)")
        if health["issues"]:
            for issue in health["issues"]:
                print(f"   ⚠️  {issue}")

        # Edge Cases
        if evaluation["edge_cases"]:
            print(f"\n⚠️  EDGE CASES DETECTED:")
            for case in evaluation["edge_cases"]:
                print(f"   {case}")
        else:
            print(f"\n✅ No edge cases detected in this preference profile.")

        # Recommendations with confidence
        print(f"\n🎵 TOP {len(evaluation['recommendations'])} RECOMMENDATIONS:")
        for idx, rec in enumerate(evaluation["recommendations"], start=1):
            song = rec["song"]
            print(f"\n{idx}. {song['title']} - {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"   Energy: {song['energy']:.2f} | Valence: {song['valence']:.2f} | Danceability: {song['danceability']:.2f}")
            print(f"   Score: {rec['score']:.2f} | Confidence: {rec['confidence_label']}")
            print(f"   Why: {rec['explanation']}")
            print(f"   Confidence reasoning: {rec['confidence_reasoning']}")

        # Bias Analysis
        print(f"\n📈 BIAS ANALYSIS:")
        bias = evaluation["bias_report"]
        print(f"   Genre distribution: {bias['genre_distribution']}")
        print(f"   {bias['message']}")
        print(f"   Mood distribution: {bias['mood_distribution']}")

        print(f"\n{'='*80}\n")


def run_demo_with_evaluation() -> None:
    """
    Demonstration of the full system with multiple profiles.
    Shows how reliability evaluation catches edge cases and biases.
    """
    system = InteractiveRecommenderSystem()

    # Define test profiles
    profiles = {
        "High-Energy Pop Lover": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.8,
            "danceability": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi Vibe": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.55,
            "danceability": 0.5,
            "likes_acoustic": True,
        },
        "Edge Case: Upbeat Sadness": {
            # This is a contradiction - high energy but sad mood
            "genre": "pop",
            "mood": "sad",
            "energy": 0.85,
            "valence": 0.25,
            "danceability": 0.65,
            "likes_acoustic": False,
        },
        "Extreme Preferences": {
            # Very specific tastes - will reduce diversity
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "valence": 0.1,
            "danceability": 0.1,
            "likes_acoustic": False,
        },
        "Balanced Explorer": {
            # Middle-ground preferences
            "genre": "indie",
            "mood": "relaxed",
            "energy": 0.5,
            "valence": 0.6,
            "danceability": 0.55,
            "likes_acoustic": True,
        },
    }

    # Run evaluation for each profile
    for profile_name, prefs in profiles.items():
        evaluation = system.recommend_with_evaluation(prefs, k=5)
        system.print_evaluation_report(evaluation, profile_name)

    # Print system logging summary
    print(f"\n{'='*80}")
    print("📋 SYSTEM LOGGING SUMMARY")
    print(f"{'='*80}")
    log_summary = system.evaluator.logger.get_summary()
    print(f"Total events logged: {log_summary['total_events']}")
    print(f"Event types: {log_summary['event_types']}")
    print(f"{'='*80}\n")


def run_interactive_mode() -> None:
    """
    Interactive mode: user can input preferences and get evaluated recommendations.
    Good for testing and live demonstration.
    """
    system = InteractiveRecommenderSystem()

    print("\n" + "="*80)
    print("🎵 INTERACTIVE MUSIC RECOMMENDER WITH RELIABILITY EVALUATION")
    print("="*80)
    print("\nEnter your music preferences to get personalized recommendations.")
    print("(Type 'quit' to exit)\n")

    while True:
        print("\n--- Enter Your Preferences ---")
        genre = input("Favorite genre (pop/lofi/rock/jazz/etc): ").strip().lower()
        if genre == "quit":
            break

        mood = input("Favorite mood (happy/chill/intense/sad/etc): ").strip().lower()
        energy_str = input("Target energy level (0.0-1.0, e.g., 0.7): ").strip()
        valence_str = input("Target valence/positivity (0.0-1.0, e.g., 0.8): ").strip()
        danceability_str = input("Target danceability (0.0-1.0, e.g., 0.7): ").strip()
        acoustic = input("Prefer acoustic songs? (yes/no): ").strip().lower() == "yes"

        try:
            prefs = {
                "genre": genre,
                "mood": mood,
                "energy": float(energy_str),
                "valence": float(valence_str),
                "danceability": float(danceability_str),
                "likes_acoustic": acoustic,
            }

            evaluation = system.recommend_with_evaluation(prefs, k=5)
            system.print_evaluation_report(evaluation, "Your Preferences")

        except (ValueError, KeyError) as e:
            print(f"❌ Error processing preferences: {e}")
            print("   Please enter valid numbers (0.0-1.0 for numeric fields)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Music Recommender with Reliability Evaluation")
    parser.add_argument(
        "--mode",
        choices=["demo", "interactive"],
        default="demo",
        help="Run mode: 'demo' shows example profiles, 'interactive' lets you enter preferences"
    )

    args = parser.parse_args()

    if args.mode == "interactive":
        run_interactive_mode()
    else:
        run_demo_with_evaluation()
