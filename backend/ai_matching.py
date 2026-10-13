
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Load the AI model only when a similarity calculation is needed
model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return model


# Minimum score required to display a match
MIN_MATCH_SCORE = 50.0


def normalize_text(text: str) -> str:
    """Normalize text to make comparisons consistent."""
    text = str(text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two text values.
    Returns a score between 0 and 100.
    """
    if not str(text1 or "").strip() or not str(text2 or "").strip():
        return 0.0

    current_model = get_model()

    embeddings = current_model.encode(
        [text1, text2],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = max(0.0, float(similarity)) * 100

    return round(min(score, 100.0), 2)


def create_item_text(item: dict) -> str:
    """Create a combined text representation of an item."""
    return (
        f"Item name: {item.get('item_name', '')}. "
        f"Description: {item.get('description', '')}. "
        f"Location: {item.get('location', '')}."
    )


def calculate_item_similarity(item1: dict, item2: dict) -> float:
    """
    Compare item names, descriptions, and locations separately.

    Name:        50%
    Description: 35%
    Location:    15%
    """
    name1 = str(item1.get("item_name", "") or "").strip()
    name2 = str(item2.get("item_name", "") or "").strip()

    description1 = str(item1.get("description", "") or "").strip()
    description2 = str(item2.get("description", "") or "").strip()

    location1 = str(item1.get("location", "") or "").strip()
    location2 = str(item2.get("location", "") or "").strip()

    name_score = calculate_text_similarity(name1, name2)
    description_score = calculate_text_similarity(
        description1, description2
    )
    location_score = calculate_text_similarity(
        location1, location2
    )

    final_score = (
        name_score * 0.50
        + description_score * 0.35
        + location_score * 0.15
    )

    return round(final_score, 2)


def create_duplicate_key(item: dict) -> tuple:
    """Identify repeated item reports using normalized text."""
    return (
        normalize_text(item.get("item_name", "")),
        normalize_text(item.get("description", "")),
        normalize_text(item.get("location", ""))
    )


def find_matching_items(lost_item: dict, found_items: list) -> list:
    """
    Find relevant matching items using semantic similarity,
    duplicate removal, a minimum score, and descending sorting.
    """
    matches = []
    seen_items = set()

    for candidate in found_items:
        if "_id" not in candidate:
            continue

        duplicate_key = create_duplicate_key(candidate)

        if duplicate_key in seen_items:
            continue

        seen_items.add(duplicate_key)

        score = calculate_item_similarity(lost_item, candidate)

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
