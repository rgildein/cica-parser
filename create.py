import logging
import sys
from datetime import datetime

from tqdm import tqdm

from utils.data import save_data
from utils.logger import set_up_logger
from utils.parser import get_cadastral_areas, get_districts, get_owner_list, get_surnames, LETTERS

logger = logging.getLogger(__name__)


def get_owners(output_file: str, district: str, cadastral_area: str, letter: str, surname: str) -> None:
    """get list of owners and save it"""
    data = []
    for owner in get_owner_list(district, cadastral_area, letter, surname):
        data.append([district, cadastral_area, letter, surname, owner])
    save_data(output_file, data)  # save data


def get_data():
    """get data from cica"""
    output_file = f"cica-{datetime.now():%Y%m%d-%H%M}.csv"

    for district in tqdm(get_districts(), desc="district"):
        for cadastral_area in tqdm(get_cadastral_areas(district), desc="cad. area", leave=False):
            for letter in tqdm(LETTERS, desc="letter", leave=False):
                for surname in tqdm(get_surnames(district, cadastral_area, letter), desc="surname", leave=False):
                    get_owners(output_file, district, cadastral_area, letter, surname)


def main(debug: bool, console: bool):
    set_up_logger(debug, console),
    get_data()


if __name__ == "__main__":
    main(any([argv == "--debug" for argv in sys.argv]), any([argv == "--console" for argv in sys.argv]))
