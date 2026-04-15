from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs sorted by descending relevance score."""
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = self._score_song_model(user, song)
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short plain-language explanation for one song."""
        score, reasons = self._score_song_model(user, song)
        reason_text = "; ".join(reasons)
        return f"{reason_text}. Total score: {score:.2f}."

    def _score_song_model(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_similarity = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        energy_points = energy_similarity * 2.0
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

        likes_acoustic_song = song.acousticness >= 0.6
        if likes_acoustic_song == user.likes_acoustic:
            score += 0.75
            reasons.append("acoustic preference match (+0.75)")

        return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    weights = user_prefs.get("weights", {})
    genre_weight = float(weights.get("genre", 2.0))
    mood_weight = float(weights.get("mood", 1.0))
    energy_weight = float(weights.get("energy", 2.0))
    valence_weight = float(weights.get("valence", 1.0))
    danceability_weight = float(weights.get("danceability", 1.0))
    acoustic_weight = float(weights.get("acoustic", 0.75))

    preferred_genre = str(user_prefs.get("genre", "")).lower()
    preferred_mood = str(user_prefs.get("mood", "")).lower()

    if preferred_genre and song["genre"].lower() == preferred_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.2f})")

    if preferred_mood and song["mood"].lower() == preferred_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.2f})")

    if "energy" in user_prefs:
        target_energy = float(user_prefs["energy"])
        energy_similarity = max(0.0, 1.0 - abs(song["energy"] - target_energy))
        energy_points = energy_similarity * energy_weight
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    if "valence" in user_prefs:
        target_valence = float(user_prefs["valence"])
        valence_similarity = max(0.0, 1.0 - abs(song["valence"] - target_valence))
        valence_points = valence_similarity * valence_weight
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    if "danceability" in user_prefs:
        target_dance = float(user_prefs["danceability"])
        dance_similarity = max(0.0, 1.0 - abs(song["danceability"] - target_dance))
        dance_points = dance_similarity * danceability_weight
        score += dance_points
        reasons.append(f"danceability closeness (+{dance_points:.2f})")

    if "likes_acoustic" in user_prefs:
        likes_acoustic_song = song["acousticness"] >= 0.6
        if bool(user_prefs["likes_acoustic"]) == likes_acoustic_song:
            score += acoustic_weight
            reasons.append(f"acoustic preference match (+{acoustic_weight:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
