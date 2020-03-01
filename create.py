import logging
import sys
from datetime import datetime

import pandas as pd

from tqdm import tqdm

from utils.logger import set_up_logger
from utils.parser import get_districts, get_cadastral_areas, get_surnames, get_owner_list

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "CH", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

logger = logging.getLogger(__name__)


def get_data():
    """get data from cica"""
    data = []
    try:
        for district in tqdm(get_districts(), desc="district"):
            for cadastral_area in tqdm(get_cadastral_areas(district), desc="cad. area", leave=False):
                for letter in tqdm(LETTERS, desc="letter", leave=False):
                    for surname in tqdm(get_surnames(district, cadastral_area, letter), desc="surname", leave=False):
                        for owner in get_owner_list(district, cadastral_area, letter, surname):
                            data.append([district, cadastral_area, letter, surname, owner])
    except Exception as error:
        logger.error(error)

    return data


def main(debug: bool = False):
    set_up_logger(debug)
    data = get_data()
    df = pd.DataFrame(data=data, columns=["okres", "katastralne uzemie", "prve pismeno", "priezvisko", "vlastnik"])
    df.to_csv(f"cica-{datetime.now():%Y%m%d-%H%M}'.csv", sep=";")


if __name__ == "__main__":
    main(any([argv == "--debug" for argv in sys.argv]))
