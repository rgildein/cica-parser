import logging
from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from utils.selenium import (
    get_select_options,
    get_selected_value,
    select_value,
    wait_until_empty_select,
    wait_until_value_change,
)

STEPS_ORDER = ["district", "cadastral_area", "letter", "surname"]
TIMEOUT = 5
logger = logging.getLogger(__name__)


@contextmanager
def cica():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        cica_initialized(driver)
        yield driver
    finally:
        driver.quit()


def cica_initialized(driver: webdriver):
    """initialized cica page"""
    driver.get("https://cica.vugk.sk/Default.aspx")
    driver.find_element_by_id("button_VL").click()
    logger.info("cica page was initialized")


def cica_steps(
    driver: webdriver,
    district: Optional[str] = None,
    cadastral_area: Optional[str] = None,
    letter: Optional[str] = None,
    surname: Optional[str] = None,
    refresh: bool = False,
) -> None:
    """execute step on page refresh"""
    # refresh page
    if refresh:
        cica_initialized(driver)

    if district and district != get_selected_value(driver, "DropDownList_okres"):
        original_cadastral_area = get_selected_value(driver, "DropDownList_ku")
        select_value(driver, "DropDownList_okres", district)
        wait_until_value_change(driver, "DropDownList_ku", original_cadastral_area)
        logger.info(f"district `{district}` was successfully changed")

    if cadastral_area and cadastral_area != get_selected_value(driver, "DropDownList_ku"):
        original_commune = get_selected_value(driver, "DropDownList_obec")
        select_value(driver, "DropDownList_ku", cadastral_area)
        wait_until_value_change(driver, "DropDownList_obec", original_commune)
        logger.info(f"cadastral_area `{cadastral_area}` was successfully changed")

    if letter and letter != get_selected_value(driver, "DropDownList_ABC"):
        select_value(driver, "DropDownList_ABC", letter)
        wait_until_empty_select(driver, "DropDownList_VL_PRI")
        logger.info(f"letter `{letter}` was successfully changed")

    if surname and surname != get_selected_value(driver, "DropDownList_VL_PRI"):
        original_surname = get_selected_value(driver, "DropDownList_VL")
        select_value(driver, "DropDownList_VL_PRI", surname)
        wait_until_value_change(driver, "DropDownList_VL", original_surname)
        logger.info(f"surname `{surname}` was successfully changed")


def cica_execute(
    parse: Callable, driver: webdriver, steps: Optional[Dict[str, str]] = None, count: int = 0, max_try: int = 3,
) -> Any:
    """execute one step on cica page"""
    steps = steps or {}
    try:
        cica_steps(driver, **steps, refresh=count > 0)
        return parse()
    except Exception as error:
        logger.exception(error)
        if count + 1 < max_try:
            return cica_execute(parse, driver, steps, count + 1, max_try)
        else:
            raise error


def get_districts(driver: webdriver, **kwargs) -> List[str]:
    """get list of districts"""

    def parse():
        options = get_select_options(driver, "DropDownList_okres")
        return [district.value for district in options]

    return cica_execute(parse, driver, **kwargs)


def get_cadastral_areas(driver: webdriver, district: str, **kwargs) -> List[str]:
    """get list of cadastral area"""

    def parse():
        options = get_select_options(driver, "DropDownList_ku")
        return [ca.value for ca in options]

    return cica_execute(parse, driver, steps={"district": district}, **kwargs)


def get_letters(driver: webdriver, district: str, cadastral_area: str, **kwargs) -> List[str]:
    """get list of letters"""

    def parse():
        options = get_select_options(driver, "DropDownList_ABC")
        return [letter.value for letter in options]

    return cica_execute(parse, driver, steps={"district": district, "cadastral_area": cadastral_area}, **kwargs,)


def get_surnames(driver: webdriver, district: str, cadastral_area: str, letter: str, **kwargs) -> List[str]:
    """get list of surnames"""

    def parse():
        options = get_select_options(driver, "DropDownList_VL_PRI")
        return [surname.value for surname in options if not surname.text.startswith("Nie je vlastník začínajúci na")]

    return cica_execute(
        parse, driver, steps={"district": district, "cadastral_area": cadastral_area, "letter": letter}, **kwargs,
    )


def get_owner_list(
    driver: webdriver, district: str, cadastral_area: str, letter: str, surname: str, **kwargs
) -> List[str]:
    """get list of owners"""

    def parse():
        options = get_select_options(driver, "DropDownList_VL")
        return [owner.value for owner in options]

    return cica_execute(
        parse,
        driver,
        steps={"district": district, "cadastral_area": cadastral_area, "letter": letter, "surname": surname},
        **kwargs,
    )
