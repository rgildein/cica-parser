import logging
import time
from contextlib import contextmanager
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select

from utils.selenium import wait_until_click, wait_until_not_empty, wait_until_find

LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "CH",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
TIMEOUT = 5
logger = logging.getLogger(__name__)


@contextmanager
def cica(
    district: Optional[str] = None,
    cadastral_area: Optional[str] = None,
    first_letter: Optional[str] = None,
    surname: Optional[str] = None,
):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get("https://cica.vugk.sk/Default.aspx")
        driver.find_element_by_id("button_VL").click()
        logger.info("cica page was initialized")

        if district:
            wait_until_click(driver, "DropDownList_okres", district)

            if cadastral_area:
                wait_until_click(driver, "DropDownList_ku", cadastral_area)

                if first_letter:
                    time.sleep(1)  # wait for refresh
                    wait_until_click(driver, "DropDownList_ABC", first_letter)

                    if surname:
                        wait_until_click(driver, "DropDownList_VL_PRI", surname)
        yield driver
    finally:
        driver.quit()


def get_districts() -> List[str]:
    """get list of districts"""
    with cica() as driver:
        return [district.text for district in Select(wait_until_find(driver, "DropDownList_okres")).options]


def get_cadastral_areas(district: str) -> List[str]:
    """get list of cadastral area"""
    with cica(district) as driver:
        return [cadastral_area.text for cadastral_area in Select(wait_until_find(driver, "DropDownList_ku")).options]


def get_first_letters(district: str, cadastral_area: str) -> List[str]:
    """get list of first letters of surname"""
    with cica(district, cadastral_area) as driver:
        return [first_letter.text for first_letter in Select(wait_until_find(driver, "DropDownList_ABC")).options]


def get_surnames(district: str, cadastral_area: str, first_letter: str) -> List[str]:
    """get list of surnames"""
    with cica(district, cadastral_area, first_letter) as driver:
        return [surname.text for surname in Select(wait_until_find(driver, "DropDownList_VL_PRI")).options]


def get_owner_list(district: str, cadastral_area: str, first_letter: str, surname: str) -> List[str]:
    """get list of owners"""
    with cica(district, cadastral_area, first_letter, surname) as driver:
        return [owner.text for owner in Select(wait_until_find(driver, "DropDownList_VL")).options]
