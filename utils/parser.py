import logging
from contextlib import contextmanager
from typing import List, Optional

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.wrapper import tries

logger = logging.getLogger(__name__)


@contextmanager
def cica(
        district: Optional[str] = None,
        cadastral_area: Optional[str] = None,
        first_letter: Optional[str] = None,
        surname: Optional[str] = None,
):
    options = Options()
    options.add_argument('--headless')
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
                    time.sleep(1)  # wait until refresh page
                    wait_until_click(driver, "DropDownList_ABC", first_letter)

                    if surname:
                        wait_until_click(driver, "DropDownList_VL_PRI", surname)
        yield driver
    finally:
        driver.close()


def wait_until_not_empty(driver: webdriver.Firefox, select_id: str) -> None:
    """wait until select is not empty"""
    WebDriverWait(driver, 2).until(
        expected_conditions.element_to_be_clickable((By.XPATH, f"//select[@id='{select_id}']/option[@value!='']")),
        f"element {select_id} was not found with not empty value",
    )
    logger.debug(f"element {select_id} was found with not empty value")


def wait_until_click(driver: webdriver.Firefox, select_id: str, value: str) -> None:
    """wait util select value"""
    wait_until_not_empty(driver, select_id)
    WebDriverWait(driver, 2).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, f"//select[@id='{select_id}']/option[@value='{value}']")
        ),
        f"value {value} at element {select_id} was not found",
    ).click()
    logger.debug(f"value {value} at element {select_id} was found")


def wait_until_find(driver: webdriver.Firefox, select_id: str) -> webelement:
    """wait until find select"""
    wait_until_not_empty(driver, select_id)
    element = WebDriverWait(driver, 2).until(
        expected_conditions.element_to_be_clickable((By.XPATH, f"//select[@id='{select_id}']")),
        f"element {select_id} was not found",
    )
    logger.debug(f"element {select_id} was found")
    return element


@tries
def get_districts() -> List[str]:
    """get list of districts"""
    with cica() as driver:
        return [district.text for district in Select(wait_until_find(driver, "DropDownList_okres")).options]


@tries
def get_cadastral_areas(district: str) -> List[str]:
    """get list of cadastral area"""
    with cica(district) as driver:
        return [cadastral_area.text for cadastral_area in Select(wait_until_find(driver, "DropDownList_ku")).options]


@tries
def get_first_letters(district: str, cadastral_area: str) -> List[str]:
    """get list of first letters of surname"""
    with cica(district, cadastral_area) as driver:
        return [first_letter.text for first_letter in Select(wait_until_find(driver, "DropDownList_ABC")).options]


@tries
def get_surnames(district: str, cadastral_area: str, first_letter: str) -> List[str]:
    """get list of surnames"""
    with cica(district, cadastral_area, first_letter) as driver:
        return [surname.text for surname in Select(wait_until_find(driver, "DropDownList_VL_PRI")).options]


@tries
def get_owner_list(district: str, cadastral_area: str, first_letter: str, surname: str) -> List[str]:
    """get list of owners"""
    with cica(district, cadastral_area, first_letter, surname) as driver:
        return [owner.text for owner in Select(wait_until_find(driver, "DropDownList_VL")).options]
