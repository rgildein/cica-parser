import logging

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils.wrapper import tries

TIMEOUT = 5
logger = logging.getLogger(__name__)


class WaitUntilNotEmptySelect(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            options = expected_conditions._find_elements(driver, self.locator)
            if len(options) == 0:
                return False
            elif len(options) == 1 and not options[0].text:
                return False
            else:
                return True
        except StaleElementReferenceException:
            return False


@tries
def wait_until_empty(driver: webdriver, select_id: str) -> None:
    """wait until select is not empty"""

    WebDriverWait(driver, TIMEOUT).until(
        WaitUntilNotEmptySelect((By.XPATH, f"//select[@id='{select_id}']/option")),
        f"element {select_id} was not found with not empty value",
    )
    logger.debug(f"element {select_id} was found with not empty value")


@tries
def wait_until_click(driver: webdriver, select_id: str, value: str) -> None:
    """wait util select value"""
    wait_until_empty(driver, select_id)
    WebDriverWait(driver, TIMEOUT).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, f"//select[@id='{select_id}']/option[@value='{value}']")
        ),
        f"value {value} at element {select_id} was not found",
    ).click()
    logger.debug(f"value {value} at element {select_id} was found")


@tries
def wait_until_find(driver: webdriver, select_id: str) -> webelement:
    """wait until find select"""
    wait_until_empty(driver, select_id)
    element = WebDriverWait(driver, TIMEOUT).until(
        expected_conditions.element_to_be_clickable((By.XPATH, f"//select[@id='{select_id}']")),
        f"element {select_id} was not found",
    )
    logger.debug(f"element {select_id} was found")
    return element
