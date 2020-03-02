import collections

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select

OPTION = collections.namedtuple("option", "text value")


class WaitUntilReadySelect(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            if element and element.is_enabled() and element.is_displayed():
                return element
            else:
                return False
        except WebDriverException:
            return False


class WaitUntilEmptySelect(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            options = Select(element).options
            return not(options[0].text == "" and len(options) == 1)
        except (WebDriverException, IndexError):
            return False


class WaitUntilChangedSelect(WaitUntilReadySelect):
    def __init__(self, locator, exp_value):
        super().__init__(locator)
        self.exp_value = exp_value

    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            return element.get_attribute("value") != self.exp_value
        except WebDriverException:
            return False


class WaitUntilValueSelect(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            return element.get_attribute("value") or "--empty--"
        except WebDriverException:
            return False


class WaitUntilSelectOptions(WaitUntilReadySelect):
    def __call__(self, driver):
        try:
            element = super().__call__(driver)
            return [
                OPTION(text=option.text, value=option.get_attribute("value"))
                for option in Select(element).options
                if option.text != ""
            ]
        except WebDriverException:
            return False
