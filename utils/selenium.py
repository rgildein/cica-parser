import logging
from typing import List, NamedTuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.expected_conditions import (
    WaitUntilChangedSelect,
    WaitUntilEmptySelect,
    WaitUntilReadySelect,
    WaitUntilSelectOptions,
    WaitUntilValueSelect,
)

TIMEOUT = 20
Option = NamedTuple("option", [("text", str), ("value", str)])
logger = logging.getLogger(__name__)


def get_select_options(driver: webdriver, select_id: str) -> List[Option]:
    """get all select options"""
    return WebDriverWait(driver, TIMEOUT).until(
        WaitUntilSelectOptions((By.XPATH, f"//select[@id='{select_id}']")), f"element `{select_id}` could not be found",
    )


def get_selected_value(driver: webdriver, select_id: str) -> str:
    """get actual selected value"""
    value = WebDriverWait(driver, TIMEOUT).until(
        WaitUntilValueSelect((By.XPATH, f"//select[@id='{select_id}']/option[@selected='selected']")),
        f"element '{select_id}' has no selected value",
    )
    return value if value != "--empty--" else ""


def select_value(driver: webdriver, select_id: str, value: str) -> None:
    """select value"""
    element = WebDriverWait(driver, TIMEOUT).until(
        WaitUntilReadySelect((By.XPATH, f"//select[@id='{select_id}']/option[@value='{value}']")),
        f"value `{value}` at element `{select_id}` was not found",
    )
    element.click()  # click element


def wait_until_value_change(driver: webdriver, select_id: str, exp_value: str) -> None:
    """wait while select does not changed value"""
    WebDriverWait(driver, TIMEOUT).until(
        WaitUntilChangedSelect((By.XPATH, f"//select[@id='{select_id}']/option[@selected='selected']"), exp_value),
        f"element `{select_id}` has not changed value `{exp_value}`",
    )


def wait_until_empty_select(driver: webdriver, select_id: str) -> None:
    """waith while select is empty"""
    WebDriverWait(driver, TIMEOUT).until(
        WaitUntilEmptySelect((By.XPATH, f"//select[@id='{select_id}']")), f"element `{select_id}` is empty",
    )
