def normalize_alias(value: str) -> str:
    value = str(value or "").strip().lower()
    return " ".join(value.split())
