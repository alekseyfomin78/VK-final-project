import allure
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from ui.locators.locators import LoginPageLocators


class ErrorLoginException(Exception):
    pass


class LoginPage(BasePage):

    locators = LoginPageLocators()
    url = 'http://127.0.0.1:8086/login'

    @allure.step('Login')
    def login(self, username, password):
        elem_username = self.find(self.locators.USERNAME_LOCATOR)
        elem_username.clear()
        elem_username.send_keys(username)

        elem_password = self.find(self.locators.PASSWORD_LOCATOR)
        elem_password.clear()
        elem_password.send_keys(password)

        self.click(self.locators.LOGIN_BUTTON_LOCATOR)

        # успешная авторизация - переход на главной страницу
        if self.driver.current_url == MainPage.url:
            return MainPage(self.driver)

        # неуспешная авторизация - появляется сообщение об ошибке
        if self.element_is_visibility(self.locators.ERROR_LOGIN_MESSAGE_LOCATOR):
            raise ErrorLoginException(f'Invalid username: {username} or password: {password}')

    @allure.step('Go to registration page')
    def go_to_registration_page(self) -> RegistrationPage:
        href_to_reg_page = self.find(self.locators.GO_TO_REGISTRATION_PAGE_LOCATOR)
        self.click(href_to_reg_page)
        return RegistrationPage(self.driver)
