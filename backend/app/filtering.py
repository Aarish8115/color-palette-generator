import pandas as pd


def apply_color_name_filter(df: pd.DataFrame, matched_row_ids: dict) -> pd.DataFrame:
    """
    Restricts df to rows whose index appears in any of the matched 
    color name row-ID lists (union across all matched words).
    """
    if not matched_row_ids:
        return df

    all_ids = set()
    for ids in matched_row_ids.values():
        all_ids.update(ids)

    return df[df.index.isin(all_ids)]


def apply_constraint_filter(df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Applies prompt-derived constraints to the dataframe.
    Current constraint model only uses hue_family.
    """
    if "hue_family" in constraints:
        return df[df["hue_family"] == constraints["hue_family"]]
    return df


def filter_candidates(
    df: pd.DataFrame,
    constraints: dict,
    matched_row_ids: dict,
    min_results: int = 5
) -> pd.DataFrame:
    """
    Main entry point. Combines color-name filtering and constraint 
    filtering. If constrained candidates are too few, relaxes hue_family
    while keeping explicit named-color matches as the harder signal.
    """
    # start with color-name restriction if present
    candidates = apply_color_name_filter(df, matched_row_ids)

    # apply mood/style constraints on top
    filtered = apply_constraint_filter(candidates, constraints)

    if len(filtered) >= min_results:
        return filtered

    # fallback: relax hue_family constraint if it over-constrains the pool
    if "hue_family" in constraints:
        relaxed_constraints = {k: v for k, v in constraints.items() if k != "hue_family"}
        filtered = apply_constraint_filter(candidates, relaxed_constraints)
        if len(filtered) >= min_results:
            return filtered

    # last resort: if even color-name-only filtering is too small, 
    # ignore constraints entirely; if color-name filtering itself 
    # returned nothing, fall back to the full dataset
    if len(candidates) >= min_results:
        return candidates

    return df

