import logging
from typing import List, NamedTuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.expected_conditions import (
    WaitUntilChangedSelect,
    WaitUntilEmptySelect,
    WaitUntilReadySelect,
    WaitUntilSelectOptions,
    WaitUntilValueSelect,
    WaitUntilIdSelect, WaitUntilNewSelect)

TIMEOUT = 5
Option = NamedTuple("option", [("text", str), ("value", str)])
logger = logging.getLogger(__name__)


def get_select_element_id(driver: webdriver, select_id: str) -> str:
    """get actual selected element id"""
    return WebDriverWait(driver, TIMEOUT).until(
        WaitUntilIdSelect((By.XPATH, f"//select[@id='{select_id}']/option[@selected='selected']")),
        f"element '{select_id}' has not ID",
    )


def get_select_options(driver: webdriver, select_id: str) -> List[Option]:
    """get all select options"""
    return WebDriverWait(driver, TIMEOUT).until(
        WaitUntilSelectOptions((By.XPATH, f"//select[@id='{select_id}']")), f"element `{select_id}` could not be found",
    )


def get_selected_value(driver: webdriver, select_id: str) -> str:
    """get actual selected value"""
    try:
        value = WebDriverWait(driver, TIMEOUT).until(
            WaitUntilValueSelect((By.XPATH, f"//select[@id='{select_id}']/option[@selected='selected']")),
            f"element '{select_id}' has no selected value",
        )
        return value if value != "--empty--" else ""
    except TimeoutException:
        logger.warning(f"element '{select_id}' has no selected value")
        return ""


def select_value(driver: webdriver, select_id: str, value: str) -> None:
    """select value"""
    element = WebDriverWait(driver, TIMEOUT).until(
        WaitUntilReadySelect((By.XPATH, f"//select[@id='{select_id}']/option[@value='{value}']")),
        f"value `{value}` at element `{select_id}` was not found",
    )
    element.click()  # click element


def wait_until_value_change(driver: webdriver, select_id: str, exp_value: str) -> None:
    """wait while select does not changed value"""
    try:
        WebDriverWait(driver, TIMEOUT).until(
            WaitUntilChangedSelect((By.XPATH, f"//select[@id='{select_id}']/option[@selected='selected']"), exp_value),
            f"element `{select_id}` has not changed value `{exp_value}`",
        )
    except TimeoutException:
        logger.warning(f"element `{select_id}` has not changed value `{exp_value}`")


def wait_until_empty_select(driver: webdriver, select_id: str) -> None:
    """waith while select is empty"""
    WebDriverWait(driver, TIMEOUT).until(
        WaitUntilEmptySelect((By.XPATH, f"//select[@id='{select_id}']")), f"element `{select_id}` is empty",
    )


def wait_until_new_select(driver: webdriver, select_id: str, exp_element_id: str) -> None:
    """waith while select has not new element ID"""
    WebDriverWait(driver, TIMEOUT).until(
        WaitUntilNewSelect((By.XPATH, f"//select[@id='{select_id}']"), exp_element_id),
        f"element `{select_id}` is empty",
    )
