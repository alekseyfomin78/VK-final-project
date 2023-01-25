import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):

    locators = None
    url = 'http://127.0.0.1:8086/'

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Find element')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click element')
    def click(self, locator, timeout=None):
        self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    @allure.step('Scroll to element')
    def scroll(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def element_is_visibility(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))
