import allure
from ui.pages.base_page import BasePage
from ui.locators.locators import RegistrationPageLocators


class RegistrationPage(BasePage):

    locators = RegistrationPageLocators()
    url = 'http://127.0.0.1:8086/reg'

    @allure.step('Registration')
    def registration(self, name, surname, middle_name, username, email, password, repeat_password, accept_flag=True):
        elem_name = self.find(self.locators.NAME_LOCATOR)
        elem_name.clear()
        elem_name.send_keys(name)

        elem_surname = self.find(self.locators.SURNAME_LOCATOR)
        elem_surname.clear()
        elem_surname.send_keys(surname)

        elem_middle_name = self.find(self.locators.MIDDLE_NAME_LOCATOR)
        elem_middle_name.clear()
        elem_middle_name.send_keys(middle_name)

        elem_username = self.find(self.locators.USERNAME_LOCATOR)
        elem_username.clear()
        elem_username.send_keys(username)

        elem_email = self.find(self.locators.EMAIL_LOCATOR)
        elem_email.clear()
        elem_email.send_keys(email)

        elem_password = self.find(self.locators.PASSWORD_LOCATOR)
        elem_password.clear()
        elem_password.send_keys(password)

        elem_repeat_password = self.find(self.locators.REPEAT_PASSWORD)
        elem_repeat_password.clear()
        elem_repeat_password.send_keys(repeat_password)

        if accept_flag:
            elem_accept_checkbox = self.find(self.locators.ACCEPT_CHECKBOX_LOCATOR)
            self.click(elem_accept_checkbox)

        elem_reg_button = self.find(self.locators.REGISTER_BUTTON_LOCATOR)
        self.click(elem_reg_button)
