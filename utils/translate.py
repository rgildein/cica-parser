SLOVAK_ALPHABET = {
    "á": "a",
    "ä": "a",
    "č": "c",
    "ď": "d",
    "dž": "dz",
    "é": "e",
    "í": "i",
    "ĺ": "l",
    "ľ": "l",
    "ň": "n",
    "ó": "o",
    "ô": "o",
    "ŕ": "r",
    "š": "s",
    "ť": "t",
    "ú": "u",
    "ý": "y",
    "ž": "z",
}


def remove_slovak_alphabet(text: str) -> str:
    """remove slovak alphabet from text"""
    for slovak_letter, letter in SLOVAK_ALPHABET.items():
        text = text.replace(slovak_letter, letter)
        text = text.replace(slovak_letter.upper(), letter.upper())

    return text
