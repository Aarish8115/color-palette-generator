HARMONY_RULES = {
    "subtle": {
        "secondary": {"hue_offset": 10,  "sat_delta": -5,  "light_delta": 8},
        "tertiary":  {"hue_offset": 20,  "sat_delta": -10, "light_delta": 15},
        "accent":    {"hue_offset": -15, "sat_delta": 15,  "light_delta": -5},
        "background":{"hue_offset": 5,   "sat_delta": -25, "light_delta": 30},
        "neutral":   {"hue_offset": 0,   "sat_delta": -30, "light_delta": 20},
    },
    "monochrome": {
        "secondary": {"hue_offset": 0, "sat_delta": -15, "light_delta": 15},
        "tertiary":  {"hue_offset": 0, "sat_delta": -25, "light_delta": 30},
        "accent":    {"hue_offset": 0, "sat_delta": 20,  "light_delta": -10},
        "background":{"hue_offset": 0, "sat_delta": -35, "light_delta": 40},
        "neutral":   {"hue_offset": 0, "sat_delta": -40, "light_delta": 10},
    },
    "complementary": {
        "secondary": {"hue_offset": 180, "sat_delta": 0,   "light_delta": 5},
        "tertiary":  {"hue_offset": 160, "sat_delta": -10, "light_delta": 15},
        "accent":    {"hue_offset": 200, "sat_delta": 20,  "light_delta": -5},
        "background":{"hue_offset": 0,   "sat_delta": -30, "light_delta": 35},
        "neutral":   {"hue_offset": 180, "sat_delta": -25, "light_delta": 10},
    },
    "analogous": {
        "secondary": {"hue_offset": 30,  "sat_delta": -5,  "light_delta": 8},
        "tertiary":  {"hue_offset": -30, "sat_delta": -5,  "light_delta": 8},
        "accent":    {"hue_offset": 60,  "sat_delta": 15,  "light_delta": -5},
        "background":{"hue_offset": 15,  "sat_delta": -30, "light_delta": 35},
        "neutral":   {"hue_offset": 0,   "sat_delta": -30, "light_delta": 15},
    },
    "triadic": {
        "secondary": {"hue_offset": 120, "sat_delta": 0,   "light_delta": 5},
        "tertiary":  {"hue_offset": 240, "sat_delta": 0,   "light_delta": 5},
        "accent":    {"hue_offset": 60,  "sat_delta": 20,  "light_delta": -5},
        "background":{"hue_offset": 0,   "sat_delta": -30, "light_delta": 35},
        "neutral":   {"hue_offset": 180, "sat_delta": -25, "light_delta": 10},
    },
    "vibrant": {
        "secondary": {"hue_offset": 45,  "sat_delta": 15,  "light_delta": 0},
        "tertiary":  {"hue_offset": -45, "sat_delta": 15,  "light_delta": 0},
        "accent":    {"hue_offset": 90,  "sat_delta": 25,  "light_delta": 5},
        "background":{"hue_offset": 0,   "sat_delta": -35, "light_delta": 30},
        "neutral":   {"hue_offset": 0,   "sat_delta": -30, "light_delta": 15},
    },
}

ROLE_PROFILES = {
    "subtle": {
        "secondary":  {"sat_range": (15, 45), "light_range": (35, 65)},
        "tertiary":   {"sat_range": (10, 40), "light_range": (30, 70)},
        "accent":     {"sat_range": (35, 60), "light_range": (40, 60)},  
        "background": {"sat_range": (0, 15),  "light_range": (88, 100)},
        "neutral":    {"sat_range": (0, 12),  "light_range": (45, 55)},
    },
    "monochrome": {
        "secondary":  {"sat_range": (10, 50), "light_range": (25, 75)},
        "tertiary":   {"sat_range": (5, 40),  "light_range": (15, 85)},
        "accent":     {"sat_range": (30, 55), "light_range": (35, 65)},
        "background": {"sat_range": (0, 10),  "light_range": (90, 100)},
        "neutral":    {"sat_range": (0, 8),   "light_range": (40, 60)},
    },
    "complementary": {
        "secondary":  {"sat_range": (40, 80), "light_range": (30, 65)},
        "tertiary":   {"sat_range": (30, 65), "light_range": (25, 70)},
        "accent":     {"sat_range": (65, 100),"light_range": (35, 60)},
        "background": {"sat_range": (0, 15),  "light_range": (85, 100)},
        "neutral":    {"sat_range": (0, 15),  "light_range": (40, 60)},
    },
    "analogous": {
        "secondary":  {"sat_range": (30, 65), "light_range": (30, 70)},
        "tertiary":   {"sat_range": (25, 60), "light_range": (30, 70)},
        "accent":     {"sat_range": (55, 100), "light_range": (35, 60)},
        "background": {"sat_range": (0, 15),  "light_range": (85, 100)},
        "neutral":    {"sat_range": (0, 12),  "light_range": (45, 55)},
    },
    "triadic": {
        "secondary":  {"sat_range": (45, 85), "light_range": (30, 65)},
        "tertiary":   {"sat_range": (45, 85), "light_range": (30, 65)},
        "accent":     {"sat_range": (65, 100),"light_range": (35, 60)},
        "background": {"sat_range": (0, 15),  "light_range": (85, 100)},
        "neutral":    {"sat_range": (0, 15),  "light_range": (40, 60)},
    },
    "vibrant": {
        "secondary":  {"sat_range": (60, 100),"light_range": (35, 65)},
        "tertiary":   {"sat_range": (60, 100),"light_range": (35, 65)},
        "accent":     {"sat_range": (75, 100),"light_range": (40, 60)}, 
        "background": {"sat_range": (0, 20),  "light_range": (80, 100)},
        "neutral":    {"sat_range": (0, 15),  "light_range": (40, 60)},
    },
}

ROLE_TEMPLATES = {
    2: ["primary", "secondary"],
    3: ["primary", "secondary", "accent"],
    4: ["primary", "secondary", "tertiary", "accent"],
    5: ["primary", "secondary", "tertiary", "accent", "background"],
    6: ["primary", "secondary", "tertiary", "accent", "background", "neutral"],
}

# For each num_colors count, specifies which roles should stay 
# constrained to the original filters (hue_family, warmth, etc.) 
# versus which roles are free to move via harmony math alone.
ROLE_ANCHORING = {
    2: {
        "secondary": True,   # with only 2 colors, keep both close to the requested hue
    },
    3: {
        "secondary": True,   # brown stays present in secondary
        "accent": False,     # accent is free to pop into a different hue
    },
    4: {
        "secondary": True,
        "tertiary": True,
        "accent": False,
    },
    5: {
        "secondary": True,
        "tertiary": True,
        "accent": False,
        "background": True,
    },
    6: {
        "secondary": True,
        "tertiary": True,
        "accent": False,
        "background": True,
        "neutral": False,
    },
}