
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Minimum score required to display a match
MIN_MATCH_SCORE = 50.0


def normalize_text(text: str) -> str:
    """Normalize text for consistent comparison."""
    text = str(text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using TF-IDF and cosine similarity."""

    text1 = normalize_text(text1)
    text2 = normalize_text(text2)

    if not text1 or not text2:
        return 0.0

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(max(0.0, float(similarity)) * 100, 2)

    except ValueError:
        return 0.0


def create_item_text(item: dict) -> str:
    """Combine item information into searchable text."""
    return (
        f"{item.get('item_name', '')} "
        f"{item.get('description', '')} "
        f"{item.get('location', '')}"
    )


def calculate_item_similarity(item1: dict, item2: dict) -> float:
    """
    Compare item names, descriptions and locations.

    Name: 50%
    Description: 35%
    Location: 15%
    """

    name_score = calculate_text_similarity(
        item1.get("item_name", ""),
        item2.get("item_name", "")
    )

    description_score = calculate_text_similarity(
        item1.get("description", ""),
        item2.get("description", "")
    )

    location_score = calculate_text_similarity(
        item1.get("location", ""),
        item2.get("location", "")
    )

    final_score = (
        name_score * 0.50
        + description_score * 0.35
        + location_score * 0.15
    )

    return round(final_score, 2)


def create_duplicate_key(item: dict) -> tuple:
    """Identify duplicate reports by item details."""
    return (
        normalize_text(item.get("item_name", "")),
        normalize_text(item.get("description", "")),
        normalize_text(item.get("location", ""))
    )


def find_matching_items(lost_item: dict, found_items: list) -> list:
    """Find and rank similar items."""

    matches = []
    seen_items = set()

    for candidate in found_items:

        if "_id" not in candidate:
            continue

        duplicate_key = create_duplicate_key(candidate)

        if duplicate_key in seen_items:
            continue

        seen_items.add(duplicate_key)

        score = calculate_item_similarity(
            lost_item,
            candidate
        )

        if score < MIN_MATCH_SCORE:
            continue

        matches.append({
            "item_id": str(candidate["_id"]),
            "item_name": candidate.get("item_name", ""),
            "description": candidate.get("description", ""),
            "location": candidate.get("location", ""),
            "date": candidate.get("date", ""),
            "match_score": score
        })

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return matches
