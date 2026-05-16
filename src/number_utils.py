def is_valid_number(s: str) -> bool:
    try:
        float(s)
        return True

    except ValueError:
        return False
