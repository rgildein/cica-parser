import os

import numpy as np
import pandas as pd

from utils.data import save_data, load_data, join_tables


def test_save_data(tmpdir):
    """test save data to csv"""
    save_data(tmpdir.join("test.csv"), [["Poprad", "Poprad", "A", "Adam", "Adam"]])

    with open(tmpdir.join("test.csv"), mode="r") as file:
        lines = file.readlines()

    assert len(lines) == 2, "file have wrong number of lines"
    assert lines[0] == ";".join(["okres", "katastralne uzemie", "prve pismeno", "priezvisko", f"vlastnik{os.linesep}"])
    assert lines[1] == ";".join(["Poprad", "Poprad", "A", "Adam", f"Adam{os.linesep}"])


def test_load_data(tmpdir):
    """test load data from csv"""
    save_data(tmpdir.join("test.csv"), [["Poprad", "Poprad", "A", "Adam", "Adam"]])
    df = load_data(tmpdir.join("test.csv"))

    assert df.shape == (1, 5), "loaded data has wrong size"
    assert df.iloc[0]["okres"] == "Poprad"
    assert df.iloc[0]["katastralne uzemie"] == "Poprad"
    assert df.iloc[0]["prve pismeno"] == "A"
    assert df.iloc[0]["priezvisko"] == "Adam"
    assert df.iloc[0]["vlastnik"] == "Adam"


def test_join_data():
    """tsst join data"""
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [1, 1, 1]})
    df2 = pd.DataFrame({"A": [1, 2, 3], "B": [1, 2, 2]})
    df = join_tables([df1, df2])

    assert df.shape == (5, 2), "join table has wrong size"
    assert np.equal(df.A.values, [1, 2, 3, 2, 3]).all()
    assert np.equal(df.B.values, [1, 1, 1, 2, 2]).all()
