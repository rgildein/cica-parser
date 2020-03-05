import logging
from datetime import datetime
from typing import Tuple, List

import click
from selenium import webdriver
from tqdm import tqdm

from utils.data import save_data
from utils.logger import set_up_logger
from utils.parser import cica, get_cadastral_areas, get_districts, get_letters, get_owner_list, get_surnames
from utils.translate import remove_slovak_alphabet

logger = logging.getLogger(__name__)


def get_owners(
    output_file: str, driver: webdriver, district: str, cadastral_area: str, letter: str, surname: str
) -> None:
    """get list of owners and save it"""
    data = []
    for owner in get_owner_list(driver, district, cadastral_area, letter, surname, max_try=5):
        data.append([district, cadastral_area, letter, surname, owner])

    save_data(output_file, data)  # save data


def verify_name(name: str, validated_names: List[str]) -> bool:
    """verify that the name is listed in the names list"""
    clean_name = remove_slovak_alphabet(name.lower())
    return any([clean_name.find(s) > 0 for s in validated_names])


@click.command()
@click.option("--surnames", "-s", multiple=True, type=click.STRING, required=True)
@click.option("--debug", is_flag=True, default=False, help="logging debug mode")
@click.option("--console", is_flag=True, default=False, help="print logs to console or save it")
def download(surnames: Tuple[str], debug: bool, console: bool):
    """download name"""
    output = f"cica-{datetime.now():%Y%m%d-%H%M}"

    set_up_logger(debug, console, log_file=f"{output}.log")  # set up logger
    letters = list(set([surname[0].upper() for surname in surnames]))
    surnames = list(set([remove_slovak_alphabet(surname.lower()) for surname in surnames]))
    logger.info(f"find all names starting with: {letters}")
    logger.info(f"find all names: {surnames}")

    with cica() as driver:
        for district in tqdm(get_districts(driver), desc="district"):
            for area in tqdm(get_cadastral_areas(driver, district), desc="area", leave=False):
                for letter in tqdm(get_letters(driver, district, area), desc="letter", leave=False):
                    if letter in letters:
                        for surname in tqdm(get_surnames(driver, district, area, letter), desc="surname", leave=False):
                            if verify_name(surname, surnames):
                                get_owners(f"{output}.csv", driver, district, area, letter, surname)
                            else:
                                logger.debug(f"omit the surname {surname}")
                    else:
                        logger.debug(f"omit the letter {letter}")


if __name__ == "__main__":
    download()
