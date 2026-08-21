import re
import pickle
import pandas as pd

ENGLISH_STOPWORDS = {
    "and", "or", "the", "a", "an", "of", "in", "with", "for", 
    "on", "to", "by", "is", "at", "&"
}


# Words that describe intensity/mood, not an actual color identity.
# These get excluded from the lexicon so they don't get mistaken for 
# explicit color names later.
STOPWORDS = {
    "deep", "light", "dark", "bright", "pale", "dusty", "vivid",
    "muted", "soft", "rich", "vibrant", "warm", "cool", "pastel",
    "intense", "brilliant", "faded", "dull", "strong"
} | ENGLISH_STOPWORDS

# Optional: standard color names that might not literally appear in 
# your DB's Color Name column but are common enough that users might 
# type them. Extend this list as needed.
CSS_COLOR_NAMES = {
    "lavender", "teal", "coral", "mint", "navy", "beige", "ivory",
    "indigo", "turquoise", "crimson", "amber", "charcoal", "olive",
    "burgundy", "mustard", "peach", "lilac", "rust", "plum", "salmon"
}


def extract_color_tokens(name: str) -> list[str]:
    """
    Takes a raw Color Name string and returns cleaned, lowercase word 
    tokens. Strips anything non-alphabetic (handles junk like stray 
    hex codes accidentally appended to names).
    """
    if not isinstance(name, str):
        return []
    tokens = re.findall(r"[a-zA-Z]+", name.lower())
    return tokens


def build_lexicon(df: pd.DataFrame, name_col: str = "color_name") -> set[str]:
    """
    Builds the set of valid color-name words from every row's Color Name,
    excluding intensity/mood stopwords, merged with a standard color list.
    """
    all_tokens = set()
    for name in df[name_col]:
        all_tokens.update(extract_color_tokens(name))

    lexicon = (all_tokens - STOPWORDS) | CSS_COLOR_NAMES
    return lexicon


def build_reverse_index(
    df: pd.DataFrame,
    lexicon: set[str],
    name_col: str = "color_name",
    id_col: str = "color_id"
) -> dict[str, list]:
    """
    Maps each lexicon word to the list of row IDs whose Color Name 
    contains that word.
    """
    reverse_index: dict[str, list] = {}
    for idx, row in df.iterrows():
        tokens = extract_color_tokens(row[name_col])
        row_id = row[id_col] if id_col in df.columns else idx
        for token in tokens:
            if token in lexicon:
                reverse_index.setdefault(token, []).append(row_id)
    return reverse_index


def save_lexicon(lexicon: set[str], reverse_index: dict[str, list], path: str) -> None:
    """
    Serializes the lexicon set and reverse index together into one pickle file.
    """
    with open(path, "wb") as f:
        pickle.dump({"lexicon": lexicon, "reverse_index": reverse_index}, f)


def main():
    df = pd.read_parquet("data/cleaned-colors.parquet",engine="pyarrow")

    lexicon = build_lexicon(df)
    reverse_index = build_reverse_index(df, lexicon)

    save_lexicon(lexicon, reverse_index, "data/lexicon.pickle")

    print(f"Lexicon built: {len(lexicon)} unique color words")
    print(f"Reverse index built: {len(reverse_index)} entries")


if __name__ == "__main__":
    main()