import logging
import time
from contextlib import contextmanager
from typing import List, Dict, Callable, Any, Optional

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select

from utils.selenium import wait_until_find, wait_until_click

STEPS_ORDER = ["district", "cadastral_area", "letter", "surname"]
TIMEOUT = 5
logger = logging.getLogger(__name__)


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

    if district:
        wait_until_click(driver, "DropDownList_okres", district)
        logger.info(f"select district:`{district}`")
        time.sleep(.5)

    if cadastral_area:
        wait_until_click(driver, "DropDownList_ku", cadastral_area)
        logger.info(f"select cadastral_area:`{cadastral_area}`")
        time.sleep(.5)

    if letter:
        time.sleep(2)  # wait for refresh
        wait_until_click(driver, "DropDownList_ABC", letter)
        logger.info(f"select letter:`{letter}`")
        time.sleep(.5)

    if surname:
        wait_until_click(driver, "DropDownList_VL_PRI", surname)
        logger.info(f"select surname:`{surname}`")
        time.sleep(.5)


def get_last_step(steps: Dict[str, str] = dict) -> Dict:
    """get last step from steps"""
    if len(steps) == 0:
        return {}
    else:
        for step in STEPS_ORDER[::-1]:
            if step in steps:
                return {step: steps[step]}


def cica_execute(
    parse: Callable,
    driver: webdriver,
    steps: Optional[Dict[str, str]] = None,
    count: int = 0,
    max_try: int = 3,
) -> Any:
    """execute one step on cica page"""
    steps = steps or {}
    try:
        if count > 0:
            cica_steps(driver, **steps, refresh=True)
        else:
            last_step = get_last_step(steps)
            cica_steps(driver, **last_step)

        return parse()
    except Exception as error:
        logger.error(error)
        if count + 1 < max_try:
            return cica_execute(parse, driver, steps, count+1, max_try)
        else:
            raise error


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


def get_districts(driver: webdriver, **kwargs) -> List[str]:
    """get list of districts"""
    def parse():
        return [district.text for district in Select(wait_until_find(driver, "DropDownList_okres")).options]

    return cica_execute(parse, driver, **kwargs)


def get_cadastral_areas(driver: webdriver, district: str, **kwargs) -> List[str]:
    """get list of cadastral area"""
    def parse():
        return [cadastral_area.text for cadastral_area in Select(wait_until_find(driver, "DropDownList_ku")).options]

    return cica_execute(parse, driver, steps={"district": district}, **kwargs)


def get_letters(driver: webdriver, district: str, cadastral_area: str, **kwargs) -> List[str]:
    """get list of first letters of surname"""
    def parse():
        return [letter.text for letter in Select(wait_until_find(driver, "DropDownList_ABC")).options]

    return cica_execute(parse, driver, steps={"district": district, "cadastral_area": cadastral_area}, **kwargs)


def get_surnames(driver: webdriver, district: str, cadastral_area: str, letter: str, **kwargs) -> List[str]:
    """get list of surnames"""
    def parse():
        return [surname.text for surname in Select(wait_until_find(driver, "DropDownList_VL_PRI")).options]

    return cica_execute(
        parse, driver, steps={"district": district, "cadastral_area": cadastral_area, "letter": letter}, **kwargs,
    )


def get_owner_list(
    driver: webdriver, district: str, cadastral_area: str, letter: str, surname: str, **kwargs
) -> List[str]:
    """get list of owners"""
    def parse():
        return [owner.text for owner in Select(wait_until_find(driver, "DropDownList_VL")).options]

    return cica_execute(
        parse,
        driver,
        steps={"district": district, "cadastral_area": cadastral_area, "letter": letter, "surname": surname},
        **kwargs,
    )
