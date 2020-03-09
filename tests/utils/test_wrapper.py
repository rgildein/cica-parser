import pytest

from utils.wrapper import tries

global count


@tries(try_count=5)
def empty_func():
    global count
    count += 1
    raise ValueError("test error")


def test_tries():
    """test tries wrapper"""
    global count
    count = 0  # clean count
    with pytest.raises(ValueError):
        empty_func()  # run empty function

    assert count == 5
