"""
Command line runner for the Music Recommender Simulation with Reliability Evaluation.

This system combines:
1. Content-based music recommendations
2. Confidence scoring
3. Bias detection
4. Edge case handling
5. Structured logging and guardrails

Run modes:
- python -m src.main: Shows both basic and evaluated recommendations
- python -m src.main --mode basic: Just the original recommender
- python -m src.main --mode evaluated: Full evaluation with metrics
- python -m src.main --mode interactive: Interactive preference input
"""

import sys
import argparse
from typing import Dict

try:
    from .recommender import load_songs, recommend_songs
    from .interactive_system import InteractiveRecommenderSystem
except ImportError:
    from recommender import load_songs, recommend_songs
    from interactive_system import InteractiveRecommenderSystem


def print_profile_results(profile_name: str, user_prefs: Dict, songs: list, k: int = 5) -> None:
    """Print ranked recommendations and reasons for one profile (basic mode)."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}")
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{idx}. {song['title']} - {song['artist']} | score={score:.2f}")
        print(f"   reasons: {explanation}")


def main_basic() -> None:
    """Original basic recommendation mode."""
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded {len(songs)} songs")
    print("\n" + "="*80)
    print("🎵 BASIC MUSIC RECOMMENDER (Original Mode)")
    print("="*80)

    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.8,
            "danceability": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.55,
            "danceability": 0.5,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "valence": 0.45,
            "danceability": 0.6,
            "likes_acoustic": False,
        },
    }

    for profile_name, prefs in profiles.items():
        print_profile_results(profile_name, prefs, songs, k=5)


def main_evaluated() -> None:
    """Full evaluation mode with confidence, bias, edge cases."""
    system = InteractiveRecommenderSystem()
    
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
            "genre": "pop",
            "mood": "sad",
            "energy": 0.85,
            "valence": 0.25,
            "danceability": 0.65,
            "likes_acoustic": False,
        },
    }

    for profile_name, prefs in profiles.items():
        evaluation = system.recommend_with_evaluation(prefs, k=5)
        system.print_evaluation_report(evaluation, profile_name)


def main_interactive() -> None:
    """Interactive mode for user input."""
    from interactive_system import run_interactive_mode
    run_interactive_mode()


def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Music Recommender with Reliability Evaluation"
    )
    parser.add_argument(
        "--mode",
        choices=["basic", "evaluated", "interactive", "full"],
        default="full",
        help="Execution mode: 'basic' (original), 'evaluated' (with metrics), 'interactive' (user input), 'full' (both)"
    )

    args = parser.parse_args()

    if args.mode == "basic":
        main_basic()
    elif args.mode == "evaluated":
        main_evaluated()
    elif args.mode == "interactive":
        main_interactive()
    else:  # mode == "full"
        main_basic()
        print("\n" + "="*80 + "\n")
        main_evaluated()


if __name__ == "__main__":
    main()
