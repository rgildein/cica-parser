import logging
import sys
from datetime import datetime
from multiprocessing.pool import Pool
from typing import Tuple

from selenium import webdriver
from tqdm import tqdm

from utils.data import save_data
from utils.helpers import progress_bar_alive
from utils.logger import set_up_logger
from utils.parser import cica, get_cadastral_areas, get_districts, get_letters, get_owner_list, get_surnames

logger = logging.getLogger(__name__)


def get_owners(
    output_file: str, driver: webdriver, district: str, cadastral_area: str, letter: str, surname: str
) -> None:
    """get list of owners and save it"""
    data = []
    for owner in get_owner_list(driver, district, cadastral_area, letter, surname, max_try=5):
        data.append([district, cadastral_area, letter, surname, owner])
    save_data(output_file, data)  # save data


def get_data(args: Tuple[int, int, bool, bool]):
    """get data from cica"""
    part, n, debug, console = args
    output = f"cica-{datetime.now():%Y%m%d-%H%M}-({part+1}-{n})"
    set_up_logger(debug, console, f"{output}.log")

    with cica() as driver:
        pbar = tqdm(get_districts(driver, max_try=5)[part::n], desc=f"district #{part+1}", position=part)
        for district in pbar:
            logger.info(f"district: `{district}`")

            cadastral_areas = get_cadastral_areas(driver, district, max_try=5)
            for i0, cadastral_area in enumerate(cadastral_areas):
                logger.info(f"cadastral area: `{cadastral_area}`")

                letters = get_letters(driver, district, cadastral_area, max_try=5)
                for i1, letter in enumerate(letters):
                    logger.info(f"letter: `{letter}`")

                    for alive, surname in zip(
                            progress_bar_alive(), get_surnames(driver, district, cadastral_area, letter, max_try=5)
                    ):
                        logger.info(f"surname: `{surname}`")
                        get_owners(f"{output}.csv", driver, district, cadastral_area, letter, surname)

                        pbar.set_description(
                            f"district #{part+1} {i0+1}/{len(cadastral_areas)} {i1+1}/{len(letters)} {alive}"
                        )
                        pbar.refresh()


def main(debug: bool, console: bool, number_of_thread: int):
    with Pool(number_of_thread) as pool:
        pool.map(get_data, [(i, number_of_thread, debug, console) for i in range(number_of_thread)])


if __name__ == "__main__":
    main(
        any([argv == "--debug" for argv in sys.argv]),
        any([argv == "--console" for argv in sys.argv]),
        max([int(argv.replace("--pool=", "")) for argv in sys.argv if argv.startswith("--pool=")] or [1]),
    )
