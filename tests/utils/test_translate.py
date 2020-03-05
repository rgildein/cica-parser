import pytest

from utils.translate import remove_slovak_alphabet, verify_name


@pytest.mark.parametrize("text, exp_text", [
    ("Akosť", "Akost"),
    ("Kôlňa", "Kolna"),
    ("ježko", "jezko"),
    ("áôúľĽšŠ", "aoulLsS"),
])
def test_remove_slovak_letter(text, exp_text):
    """testing remove slovak special symbol from text"""
    assert remove_slovak_alphabet(text) == exp_text


@pytest.mark.parametrize("name, names, exp_result", [
    ("Ján", ["jan", "marek", "lukas"], True),
    ("ján", ["jan", "marek", "lukas"], True),
    ("Marek", ["jan", "marek", "lukas"], True),
    ("Ján Mama", ["jan", "marek", "lukas"], True),
    ("Lúkaš s.r.o.", ["jan", "marek", "lukas"], True),
    ("Andrej Lúkaš s.r.o.", ["jan", "marek", "lukas"], True),
    ("Júkaš s.r.o.", ["jan", "marek", "lukas"], False),
])
def test_verify_name(name, names, exp_result):
    """testing verify name"""
    assert verify_name(name, names) == exp_result
