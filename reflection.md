# Reflection Comparisons

## Profile Pair Comments

- High-Energy Pop vs Chill Lofi: High-Energy Pop pushes energetic, danceable tracks upward (for example pop/edm), while Chill Lofi moves low-energy, acoustic tracks to the top. This makes sense because energy and acoustic preference pull rankings in opposite directions.
- High-Energy Pop vs Deep Intense Rock: Both profiles like high energy, so some intense tracks overlap. The difference comes from genre and mood weights: pop/happy leans brighter and more danceable, while rock/intense rewards heavier tracks.
- Chill Lofi vs Deep Intense Rock: These outputs diverge the most. Chill Lofi favors calm and acoustic songs, while Deep Intense Rock favors high energy and intensity; shared songs tend to appear lower because only one side of the profile matches.
- Deep Intense Rock vs Edge Case (High Energy + Sad): The edge case profile still picks some intense songs due to high energy, but low-valence or sad-leaning songs rise compared with the rock profile. This shows the system can be steered by emotional features even with similar energy targets.

## Why This Matters

The comparison confirms that the recommender is sensitive to profile changes, but it can still over-repeat songs when one feature weight (especially genre) is too strong. This is a reminder that recommendation validity is not only about finding close matches, but also about balancing relevance and variety.
