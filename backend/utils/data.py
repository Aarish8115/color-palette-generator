import string
import pandas as pd




def cleanText(text):
    return (
        str(text)
        .replace(",", "")
        .translate(str.maketrans("", "", string.punctuation))
        .lower()
        .strip()
    )

COLOR_NAMES = [
    "red", "crimson", "scarlet", "maroon", "burgundy", "ruby", "cherry",

    "pink", "rose", "blush", "hot pink", "fuchsia",

    "orange", "amber", "apricot", "tangerine", "pumpkin", "coral",
    "salmon", "peach", "rust", "terracotta", "copper",

    "yellow", "gold", "golden", "mustard", "lemon", "canary", "honey",

    "green", "lime", "mint", "olive", "sage", "emerald", "forest",
    "moss", "jade", "pine", "seafoam", "chartreuse",

    "cyan", "turquoise", "teal", "aqua", "aquamarine",

    "blue", "sky blue", "baby blue", "powder blue", "azure",
    "cerulean", "cobalt", "royal blue", "navy", "midnight blue",
    "steel blue", "denim", "indigo",

    "purple", "violet", "lavender", "lilac", "plum",
    "orchid", "amethyst",

    "magenta",

    "brown", "beige", "tan", "camel", "chocolate",
    "coffee", "mocha", "walnut", "mahogany", "chestnut", "taupe",

    "grey", "gray", "silver", "slate", "ash",
    "smoke", "charcoal", "graphite",

    "black", "jet black", "onyx", "ebony",

    "white", "ivory", "cream", "pearl",
    "snow", "off white",

    "transparent"
]

def splitColor(string):
    categories=string.split(" ")
    colors=[]
    modifier=[]
    for category in categories:
        if category in COLOR_NAMES:
            colors.append(category)
        else:
            modifier.append(category)
        for color in COLOR_NAMES:
            if color in category:
                colors.append(color)
    colors=list(set(colors))
    return pd.Series({
        "family": " ".join(colors),
        "modifiers": " ".join(modifier)
    })