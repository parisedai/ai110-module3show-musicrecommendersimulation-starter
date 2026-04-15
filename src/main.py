"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def print_profile_results(profile_name: str, user_prefs: Dict, songs: list, k: int = 5) -> None:
    """Print ranked recommendations and reasons for one profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n=== {profile_name} ===")
    print(f"Preferences: {user_prefs}")
    for idx, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{idx}. {song['title']} - {song['artist']} | score={score:.2f}")
        print(f"   reasons: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

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
        "Edge Case: High Energy + Sad": {
            "genre": "pop",
            "mood": "sad",
            "energy": 0.9,
            "valence": 0.2,
            "danceability": 0.7,
            "likes_acoustic": False,
        },
    }

    for profile_name, prefs in profiles.items():
        print_profile_results(profile_name, prefs, songs, k=5)

    # Small data experiment: reduce genre impact and increase energy impact.
    experiment_profile = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.8,
        "danceability": 0.8,
        "likes_acoustic": False,
        "weights": {
            "genre": 1.0,
            "mood": 1.0,
            "energy": 4.0,
            "valence": 1.0,
            "danceability": 1.0,
            "acoustic": 0.75,
        },
    }
    print_profile_results("Experiment: Energy-Heavy Weights", experiment_profile, songs, k=5)


if __name__ == "__main__":
    main()
