import collections
from typing import Union

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

OPTION = collections.namedtuple("option", "text value")


class WaitUntilReadySelect(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver) -> Union[bool, WebElement]:
        try:
            element = driver.find_element(*self.locator)
            if element and element.is_enabled() and element.is_displayed():
                return element
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilIdSelect(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                return element.id
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilNewSelect(WaitUntilReadySelect):
    def __init__(self, locator, exp_id):
        super().__init__(locator)
        self.exp_id = exp_id

    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                return element.id != self.exp_id
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilEmptySelect(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                options = Select(element).options
                return options[0].text == "" and len(options) == 1
            else:
                return False
        except (WebDriverException, IndexError):
            return False


class WaitUntilChangedSelect(WaitUntilReadySelect):
    def __init__(self, locator, exp_value):
        super().__init__(locator)
        self.exp_value = exp_value

    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                return element.get_attribute("value") != self.exp_value
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilValueSelect(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                return element.get_attribute("value") or "--empty--"
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilSelectOptions(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            if element:
                return [
                    OPTION(text=option.text, value=option.get_attribute("value"))
                    for option in Select(element).options
                    if option.text != ""
                ]
            else:
                return False
        except WebDriverException:
            return False
