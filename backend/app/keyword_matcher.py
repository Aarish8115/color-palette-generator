from app.config_rules import KEYWORD_RULES, SYNONYMS


def expand_synonyms(prompt_text: str) -> str:
    """
    Replaces known synonym words in the prompt with their canonical form,
    so downstream keyword matching only needs to check for the canonical 
    word, not every variant.
    """
    text = prompt_text.lower()
    for canonical, variants in SYNONYMS.items():
        for variant in variants:
            if variant in text:
                text = text.replace(variant, canonical)
    return text


def match_keywords(normalized_text: str) -> dict:
    """
    Checks the normalized prompt text against KEYWORD_RULES. For every 
    phrase found, merges its filter conditions into one constraints dict.
    When two rules set the same key, keep the more restrictive value.
    """
    constraints = {}

    for phrase, rule in KEYWORD_RULES.items():
        if phrase in normalized_text:
            for key, value in rule.items():
                if key not in constraints:
                    constraints[key] = value
                else:
                    # merge conflicting numeric bounds by taking the 
                    # more restrictive (tighter) constraint
                    if key.endswith("_max"):
                        constraints[key] = min(constraints[key], value)
                    elif key.endswith("_min"):
                        constraints[key] = max(constraints[key], value)
                    else:
                        constraints[key] = value  # categorical, just overwrite

    return constraints


def extract_constraints(prompt_text: str) -> dict:
    """
    Main entry point. Expands synonyms, then matches against KEYWORD_RULES,
    returns the final merged constraints dictionary.
    """
    normalized = expand_synonyms(prompt_text)
    return match_keywords(normalized)

