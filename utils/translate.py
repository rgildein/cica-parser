from typing import List

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


def verify_name(name: str, validated_names: List[str]) -> bool:
    """verify that the name is listed in the names list"""
    clean_name = remove_slovak_alphabet(name.lower())
    return any([clean_name.find(remove_slovak_alphabet(vs.lower())) >= 0 for vs in validated_names])
