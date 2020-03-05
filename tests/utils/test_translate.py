import pytest

from utils.translate import remove_slovak_alphabet


@pytest.mark.parametrize("text, exp_text", [
    ("Akosť", "Akost"),
    ("Kôlňa", "Kolna"),
    ("ježko", "jezko"),
    ("áôúľĽšŠ", "aoulLsS"),
])
def test_remove_slovak_letter(text, exp_text):
    """testing remove slovak special symbol from text"""
    assert remove_slovak_alphabet(text) == exp_text
