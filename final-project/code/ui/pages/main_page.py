import allure
from selenium.webdriver import ActionChains

from ui.pages.base_page import BasePage
from ui.locators.locators import MainPageLocators


class MainPage(BasePage):

    locators = MainPageLocators()
    url = 'http://127.0.0.1:8086/welcome/'

    @allure.step('Go to home page')
    def go_to_home_page(self):
        elem_home = self.find(self.locators.HOME_LOCATOR)
        self.click(elem_home)

    @allure.step('Click on Logo')
    def click_logo(self):
        elem_logo = self.find(self.locators.LOGO_LOCATOR)
        self.click(elem_logo)

    @allure.step('Logout')
    def logout(self):
        elem_logout = self.find(self.locators.LOGOUT_LOCATOR)
        self.click(elem_logout)

    def go_to_page(self, locator):
        self.click(locator)
        self.driver.switch_to.window(self.driver.window_handles[-1])  # window_handles - список активных окон

    def go_to_page_in_navbar(self, name, link):
        name = self.find(name)
        link = self.find(link)
        action = ActionChains(self.driver)
        action.move_to_element(name).click(link).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

