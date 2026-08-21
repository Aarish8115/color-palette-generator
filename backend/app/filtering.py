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
    Applies numeric/categorical constraints from keyword_matcher's output
    to the dataframe. Ignores keys it doesn't recognize (safety net).
    """
    filtered = df

    if "saturation_max" in constraints:
        filtered = filtered[filtered["Saturation"] <= constraints["saturation_max"]]
    if "saturation_min" in constraints:
        filtered = filtered[filtered["Saturation"] >= constraints["saturation_min"]]
    if "lightness_max" in constraints:
        filtered = filtered[filtered["Lightness"] <= constraints["lightness_max"]]
    if "lightness_min" in constraints:
        filtered = filtered[filtered["Lightness"] >= constraints["lightness_min"]]
    if "contrast_score_max" in constraints:
        filtered = filtered[filtered["contrast_score"] <= constraints["contrast_score_max"]]
    if "contrast_score_min" in constraints:
        filtered = filtered[filtered["contrast_score"] >= constraints["contrast_score_min"]]
    if "hue_family" in constraints:
        filtered = filtered[filtered["hue_family"] == constraints["hue_family"]]
    if "warmth" in constraints:
        filtered = filtered[filtered["warmth"] == constraints["warmth"]]

    return filtered


def filter_candidates(
    df: pd.DataFrame,
    constraints: dict,
    matched_row_ids: dict,
    min_results: int = 5
) -> pd.DataFrame:
    """
    Main entry point. Combines color-name filtering and constraint 
    filtering. If the combined result is too small/empty, relaxes 
    constraints first (keeps color-name match as the harder requirement, 
    since it's an explicit user signal).
    """
    # start with color-name restriction if present
    candidates = apply_color_name_filter(df, matched_row_ids)

    # apply mood/style constraints on top
    filtered = apply_constraint_filter(candidates, constraints)

    if len(filtered) >= min_results:
        return filtered

    # fallback: drop constraints one at a time (least specific first) 
    # until we have enough candidates, but keep color-name match intact
    relaxed_constraints = constraints.copy()
    drop_order = ["contrast_score_max", "contrast_score_min", "saturation_max",
                  "saturation_min", "lightness_max", "lightness_min", 
                  "warmth", "hue_family"]

    for key in drop_order:
        if key in relaxed_constraints:
            del relaxed_constraints[key]
            filtered = apply_constraint_filter(candidates, relaxed_constraints)
            if len(filtered) >= min_results:
                return filtered

    # last resort: if even color-name-only filtering is too small, 
    # ignore constraints entirely; if color-name filtering itself 
    # returned nothing, fall back to the full dataset
    if len(candidates) >= min_results:
        return candidates

    return df

