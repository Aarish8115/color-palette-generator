import re


def extract_constraints(prompt_text: str, valid_hue_families: set[str]) -> dict:
    """
    Main entry point for prompt-derived constraints.
    Only hue_family is extracted, based on dataframe-backed values.
    """
    normalized_prompt = prompt_text.strip().lower()
    prompt_tokens = set(re.findall(r"[a-z0-9]+", normalized_prompt))

    for hue_family in sorted(valid_hue_families, key=len, reverse=True):
        normalized_hue = hue_family.strip().lower()
        if not normalized_hue:
            continue

        if " " in normalized_hue:
            pattern = rf"\b{re.escape(normalized_hue)}\b"
            if re.search(pattern, normalized_prompt):
                return {"hue_family": normalized_hue}
            continue

        if normalized_hue in prompt_tokens:
            return {"hue_family": normalized_hue}

    return {}

