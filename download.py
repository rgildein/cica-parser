import logging
from datetime import datetime
from typing import Optional, Tuple

import click
from selenium import webdriver
from tqdm import tqdm

from utils.data import save_data
from utils.logger import set_up_logger
from utils.parser import cica, get_cadastral_areas, get_districts, get_letters, get_owner_list, get_surnames
from utils.translate import remove_slovak_alphabet, verify_name

logger = logging.getLogger(__name__)


def get_owners(
    output_file: str, driver: webdriver, district: str, cadastral_area: str, letter: str, surname: str
) -> None:
    """get list of owners and save it"""
    data = []
    for owner in get_owner_list(driver, district, cadastral_area, letter, surname, max_try=5):
        data.append([district, cadastral_area, letter, surname, owner])

    save_data(output_file, data)  # save data


@click.command()
@click.option("--districts", "-d", multiple=True, type=click.STRING)
@click.option("--areas", "-a", multiple=True, type=click.STRING)
@click.option("--surnames", "-s", multiple=True, type=click.STRING)
@click.option("--headless", is_flag=True, default=True, help="run selenium in headless")
@click.option("--debug", is_flag=True, default=False, help="logging debug mode")
@click.option("--console", is_flag=True, default=False, help="print logs to console or save it")
def download(
    districts: Optional[str], areas: Optional[str], surnames: Tuple[str], headless: bool, debug: bool, console: bool
):
    """download name"""
    output = f"cica-{datetime.now():%Y%m%d-%H%M}"
    set_up_logger(debug, console, log_file=f"{output}.log")  # set up logger
    districts, areas = list(districts), list(areas)  # convert tuple to list

    logger.info(f"will be searched in districts {districts}")
    logger.info(f"will be searched in areas {areas}")
    letters = list(set([remove_slovak_alphabet(surname[0].upper()) for surname in surnames]))
    logger.info(f"will be searched letters {letters}")
    surnames = list(set([remove_slovak_alphabet(surname.lower()) for surname in surnames]))
    logger.info(f"will be searched surnames {surnames}")

    with cica(headless) as driver:
        for district in tqdm(districts or get_districts(driver), desc="district"):
            logger.info(f"district {district}")
            for area in tqdm(areas or get_cadastral_areas(driver, district), desc="area", leave=False, position=1):
                logger.info(f"area {area}")
                for letter in tqdm(
                    letters or get_letters(driver, district, area), desc="letter", leave=False, position=2,
                ):
                    logger.info(f"letter {letter}")
                    for surname in tqdm(
                        get_surnames(driver, district, area, letter), desc="surname", leave=False, position=3,
                    ):
                        if verify_name(surname, surnames):
                            logger.info(f"surname {surname}")
                            get_owners(f"{output}.csv", driver, district, area, letter, surname)
                        else:
                            logger.debug(f"omit the surname {surname}")


if __name__ == "__main__":
    download()
