import re
import pickle
from rapidfuzz import process, fuzz


def load_lexicon(path: str) -> tuple[set[str], dict[str, list]]:
    """
    Loads the precomputed lexicon set and reverse index from disk.
    Call this once at app startup, not per-request.
    """
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data["lexicon"], data["reverse_index"]


def tokenize(prompt_text: str) -> list[str]:
    """
    Same tokenization logic as the offline lexicon builder, applied 
    to the live user prompt.
    """
    return re.findall(r"[a-zA-Z]+", prompt_text.lower())


def exact_match(tokens: list[str], lexicon: set[str]) -> list[str]:
    """
    Returns tokens that are directly present in the lexicon.
    """
    return [t for t in tokens if t in lexicon]


def fuzzy_match(
    tokens: list[str],
    lexicon: set[str],
    already_matched: list[str],
    threshold: int = 85
) -> list[str]:
    """
    For tokens that did NOT exact-match, checks if they're a close 
    spelling variant of a lexicon word (catches typos). Skips tokens 
    already matched exactly, and skips very short tokens (e.g. "a", 
    "in") to avoid noisy false positives.
    """
    matched = []
    remaining = [t for t in tokens if t not in already_matched and len(t) > 4]

    for token in remaining:
        result = process.extractOne(token, lexicon, scorer=fuzz.ratio)
        if result is not None:
            best_match, score, _ = result
            if score >= threshold:
                matched.append(best_match)

    return matched


def detect_named_colors(
    prompt_text: str,
    lexicon: set[str],
    reverse_index: dict[str, list]
) -> dict:
    """
    Main entry point. Returns matched color words and their 
    corresponding database row IDs.
    """
    tokens = tokenize(prompt_text)

    exact = exact_match(tokens, lexicon)
    fuzzy = fuzzy_match(tokens, lexicon, already_matched=exact)

    # combine and dedupe, preserving first-seen order
    matched_words = list(dict.fromkeys(exact + fuzzy))

    matched_row_ids = {
        word: reverse_index.get(word, [])
        for word in matched_words
    }

    return {
        "matched_words": matched_words,
        "matched_row_ids": matched_row_ids
    }


# # At app startup (once):
# lexicon, reverse_index = load_lexicon("data/lexicon.pickle")

# # Per request:
# result = detect_named_colors(
#     "sapphire and lavender minimal palette",
#     lexicon,
#     reverse_index
# )

# print(result)
