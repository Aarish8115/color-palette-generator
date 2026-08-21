import colorsys
from app.config_rules import ROLE_PROFILES


def hex_to_hsl(hex_code: str) -> tuple[float, float, float]:
    """
    Converts a hex color code (e.g. '#E5B262') to HSL.
    Returns (h, s, l) where h is 0-360, s and l are 0-100.
    """
    hex_code = hex_code.lstrip("#")
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)  # note: colorsys returns H, L, S order

    return (h * 360, s * 100, l * 100)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """
    Converts HSL (h: 0-360, s: 0-100, l: 0-100) back to a hex color code.
    """
    h_norm = (h % 360) / 360
    s_norm = max(0, min(100, s)) / 100
    l_norm = max(0, min(100, l)) / 100

    r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)

    r255 = round(r * 255)
    g255 = round(g * 255)
    b255 = round(b * 255)

    return f"#{r255:02X}{g255:02X}{b255:02X}"


def apply_harmony_offset(
    primary_hsl: tuple[float, float, float],
    harmony_rule: dict
) -> tuple[float, float, float]:
    """
    Given a primary color's HSL and a harmony rule (hue_offset, sat_delta, 
    light_delta), computes the target HSL for the next role.
    """
    h, s, l = primary_hsl

    target_h = (h + harmony_rule["hue_offset"]) % 360
    target_s = max(0, min(100, s + harmony_rule["sat_delta"]))
    target_l = max(0, min(100, l + harmony_rule["light_delta"]))

    return (target_h, target_s, target_l)


def apply_role_modifier(target_hsl, role, palette_type):
    h, s, l = target_hsl

    profile = ROLE_PROFILES.get(palette_type, {}).get(role)
    if profile:
        sat_min, sat_max = profile["sat_range"]
        light_min, light_max = profile["light_range"]
        s = max(sat_min, min(sat_max, s))
        l = max(light_min, min(light_max, l))

    return (h, s, l)

def hsl_distance(
    hsl_a: tuple[float, float, float],
    hsl_b: tuple[float, float, float]
) -> float:
    """
    Computes distance between two HSL colors, treating hue as circular
    (since 359° and 1° are close, not far apart).
    """
    h1, s1, l1 = hsl_a
    h2, s2, l2 = hsl_b

    hue_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))

    # weight hue more heavily since it's the dominant perceptual factor
    distance = (
        (hue_diff * 1.0) ** 2 +
        (s1 - s2) ** 2 +
        (l1 - l2) ** 2
    ) ** 0.5

    return distance


def find_nearest_color(
    target_hsl: tuple[float, float, float],
    candidate_df,
    exclude_hexes: set,
    hue_col: str = "Hue",
    sat_col: str = "Saturation",
    light_col: str = "Lightness",
    hex_col: str = "hex"
):
    """
    Finds the row in candidate_df whose HSL is closest to target_hsl,
    excluding any hex codes already used in this palette.
    Returns the matched row, or None if no candidates remain.
    """
    available = candidate_df[~candidate_df[hex_col].isin(exclude_hexes)]

    if available.empty:
        return None

    best_row = None
    best_distance = float("inf")

    for _, row in available.iterrows():
        row_hsl = (row[hue_col], row[sat_col], row[light_col])
        dist = hsl_distance(target_hsl, row_hsl)
        if dist < best_distance:
            best_distance = dist
            best_row = row

    return best_row