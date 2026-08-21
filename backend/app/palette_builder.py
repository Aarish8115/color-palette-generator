import pandas as pd
from app.config_rules import HARMONY_RULES, ROLE_TEMPLATES, ROLE_ANCHORING
from app.color_math import apply_harmony_offset, apply_role_modifier, find_nearest_color
from app.filtering import apply_constraint_filter


def select_primary(ranked_df: pd.DataFrame, matched_words: list, matched_row_ids: dict):
    if ranked_df.empty:
        return None

    if matched_words:
        first_word = matched_words[0]
        first_word_ids = set(matched_row_ids.get(first_word, []))
        subset = ranked_df[ranked_df["color_id"].isin(first_word_ids)]
        if not subset.empty:
            return subset.iloc[0]

    return ranked_df.iloc[0]


def assign_explicit_roles(ranked_df, matched_words, matched_row_ids, num_colors):
    assigned = {}
    role_order = ROLE_TEMPLATES[num_colors]
    usable_words = matched_words[:num_colors]

    for i, word in enumerate(usable_words):
        role = role_order[i]
        word_ids = set(matched_row_ids.get(word, []))
        subset = ranked_df[ranked_df["color_id"].isin(word_ids)]
        if not subset.empty:
            assigned[role] = subset.iloc[0]

    return assigned


def build_anchored_pool(full_df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Full constraint filter, INCLUDING hue_family/warmth — used for roles 
    that should stay in the same color family as primary (e.g. secondary 
    staying brown when num_colors=3).
    """
    return apply_constraint_filter(full_df, constraints)


def build_free_pool(full_df: pd.DataFrame, constraints: dict) -> pd.DataFrame:
    """
    Constraint filter WITHOUT hue_family/warmth — used for roles that 
    should be free to move to a different hue via harmony rules 
    (e.g. accent, so it can genuinely pop/contrast).
    """
    free_constraints = {
        k: v for k, v in constraints.items()
        if k not in ("hue_family", "warmth")
    }
    return apply_constraint_filter(full_df, free_constraints)


def generate_remaining_roles(
    primary_row: pd.Series,
    assigned_roles: dict,
    palette_type: str,
    num_colors: int,
    anchored_pool: pd.DataFrame,
    free_pool: pd.DataFrame
) -> list:
    role_order = ROLE_TEMPLATES[num_colors]
    palette_rules = HARMONY_RULES[palette_type]
    anchoring = ROLE_ANCHORING.get(num_colors, {})

    primary_hsl = (primary_row["Hue"], primary_row["Saturation"], primary_row["Lightness"])

    result = []
    used_hexes = {primary_row["hex"]}
    used_names = {primary_row["color_name"]}

    # Keep explicit assignments unique and reserve them before generating roles.
    unique_assigned_roles = {}
    for role in role_order:
        if role == "primary" or role not in assigned_roles:
            continue

        row = assigned_roles[role]
        if row["hex"] in used_hexes or row["color_name"] in used_names:
            continue

        unique_assigned_roles[role] = row
        used_hexes.add(row["hex"])
        used_names.add(row["color_name"])

    for role in role_order:
        if role == "primary":
            result.append(("primary", primary_row))
            continue

        if role in unique_assigned_roles:
            row = unique_assigned_roles[role]
            result.append((role, row))
            continue

        role_rule = palette_rules.get(role)
        if role_rule is None:
            continue  # no rule defined for this role/palette_type combo, skip it

        target_hsl = apply_harmony_offset(primary_hsl, role_rule)
        target_hsl = apply_role_modifier(target_hsl, role, palette_type)

        # pick which pool to search based on this role's anchoring setting
        # for this num_colors count — anchored roles stay in the same 
        # hue_family as primary, free roles can move to any hue
        is_anchored = anchoring.get(role, False)
        search_pool = anchored_pool if is_anchored else free_pool

        nearest_row = find_nearest_color(
            target_hsl, search_pool, exclude_hexes=used_hexes,
            hue_col="Hue", sat_col="Saturation", light_col="Lightness", hex_col="hex"
        )

        attempts = 0
        while nearest_row is not None and nearest_row["color_name"] in used_names and attempts < 5:
            used_hexes.add(nearest_row["hex"])
            nearest_row = find_nearest_color(
                target_hsl, search_pool, exclude_hexes=used_hexes,
                hue_col="Hue", sat_col="Saturation", light_col="Lightness", hex_col="hex"
            )
            attempts += 1

        # fallback: if an anchored role's pool has nothing left (too 
        # narrow), fall back to the free pool rather than dropping the role
        if nearest_row is None and is_anchored:
            nearest_row = find_nearest_color(
                target_hsl, free_pool, exclude_hexes=used_hexes,
                hue_col="Hue", sat_col="Saturation", light_col="Lightness", hex_col="hex"
            )

        if nearest_row is not None:
            result.append((role, nearest_row))
            used_hexes.add(nearest_row["hex"])
            used_names.add(nearest_row["color_name"])

    return result


def build_palette(
    full_df: pd.DataFrame,
    ranked_df: pd.DataFrame,
    constraints: dict,
    matched_words: list,
    matched_row_ids: dict,
    palette_type: str,
    num_colors: int
) -> list:
    if ranked_df.empty:
        return []

    primary_row = select_primary(ranked_df, matched_words, matched_row_ids)

    assigned_roles = {}
    if len(matched_words) >= 2:
        assigned_roles = assign_explicit_roles(ranked_df, matched_words, matched_row_ids, num_colors)
        assigned_roles.pop("primary", None)

    anchored_pool = build_anchored_pool(full_df, constraints)
    free_pool = build_free_pool(full_df, constraints)

    palette = generate_remaining_roles(
        primary_row, assigned_roles, palette_type, num_colors, anchored_pool, free_pool
    )

    return palette