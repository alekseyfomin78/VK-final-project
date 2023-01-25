import allure
import pytest
from ui.pages.login_page import ErrorLoginException
from ui.locators.locators import MainPageLocators
from ui.tests.base import UIBase
from mysql.model import TestUsers


class TestRegistrationPositive(UIBase):
    create_user_in_db = False

    # БАГ. middle_name = None, хотя не должно быть None
    @allure.description('Проверка регистрации пользователя с middle_name')
    def test_user_registration(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username, middle_name=self.user.middle_name)

        assert self.driver.current_url == self.main_page.url
        assert self.user.username in self.main_page.find(MainPageLocators.USERNAME_LOCATOR).text
        assert self.user.name in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert self.user.surname in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert len(reg_user) == 1

    @allure.description('Проверка регистрации пользователя без middle_name')
    def test_user_registration_without_middle_name(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name='',
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username, middle_name=None)

        assert self.driver.current_url == self.main_page.url
        assert self.user.username in self.main_page.find(MainPageLocators.USERNAME_LOCATOR).text
        assert self.user.name in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert self.user.surname in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert len(reg_user) == 1


class TestRegistrationNegative(UIBase):
    create_user_in_db = False

    @allure.description('Проверка регистрации пользователя без name')
    def test_incorrect_name(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name='',
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password
        )

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username, name=None)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя без surname')
    def test_incorrect_surname(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname='',
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password
        )

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username, surname=None)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя без username')
    def test_incorrect_username(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username='',
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password
        )

        user_in_db = self.get_all_from_table(model=TestUsers, email=self.user.email, username=None)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя без email')
    def test_incorrect_email(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email='',
            password=self.user.password,
            repeat_password=self.user.password
        )

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username, email=None)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя без повторного ввода password')
    def test_incorrect_repeat_password(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=''
        )

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя без нажатия на checkbox подтверждения')
    def test_accept_flag_is_false(self):
        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password,
            accept_flag=False
        )

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(user_in_db) == 0

    @allure.description('Проверка регистрации пользователя, когда данный пользователь уже существует')
    def test_user_already_exists(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email
        )

        self.login_page.go_to_registration_page()

        self.registration_page.registration(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            repeat_password=self.user.password,
            accept_flag=False
        )

        reg_users_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert self.driver.current_url == self.registration_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(reg_users_in_db) == 1


class TestLoginPositive(UIBase):
    create_user_in_db = True

    @allure.description('Проверка логина пользователя с корректными данными')
    def test_correct_credentials(self):
        self.login_page.login(username=self.user.username, password=self.user.password)

        authorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=1)

        assert self.driver.current_url != self.login_page.url
        assert self.driver.current_url == self.main_page.url
        assert self.user.username in self.main_page.find(MainPageLocators.USERNAME_LOCATOR).text
        assert self.user.name in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert self.user.surname in self.main_page.find(MainPageLocators.NAME_SURNAME_LOCATOR).text
        assert 'VK ID' in self.main_page.find(MainPageLocators.VK_ID_LOCATOR).text
        assert len(authorized_user) == 1

    @allure.description('Проверка перехода со страницы Логина на страницу Регистрации')
    def test_go_to_registration_page(self):
        reg_page = self.login_page.go_to_registration_page()
        assert self.driver.current_url == reg_page.url


class TestLoginNegative(UIBase):
    create_user_in_db = False

    @allure.description('Проверка логина пользователя, когда этот пользователь не зарегистрирован')
    def test_user_not_created(self):
        with pytest.raises(ErrorLoginException):
            self.login_page.login(username=self.user.username, password=self.user.password)

    @allure.description('Проверка логина пользователя с несовпадающим username')
    def test_incorrect_username(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email)

        with pytest.raises(ErrorLoginException):
            self.login_page.login(username='some_username', password=self.user.password)

        unauthorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(unauthorized_user) == 1

    @allure.description('Проверка логина пользователя с несовпадающим password')
    def test_incorrect_password(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email)

        with pytest.raises(ErrorLoginException):
            self.login_page.login(username=self.user.username, password='some_password')

        unauthorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(unauthorized_user) == 1


class TestMainPage(UIBase):
    create_user_in_db = True

    @allure.description('Проверка выхода пользователя из приложения')
    def test_logout(self):
        self.login_page.login(username=self.user.username, password=self.user.password)

        authorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=1)

        assert len(authorized_user) == 1

        self.main_page.logout()

        unauthorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert self.driver.current_url == self.login_page.url
        assert self.driver.current_url != self.main_page.url
        assert len(unauthorized_user) == 1

    @allure.description('Проверка перехода с Главной страницы по ссылкам')
    @pytest.mark.parametrize("link, expected_url", [
        (MainPageLocators.WHAT_IS_AN_API_LOCATOR,
         "https://en.wikipedia.org/wiki/API"),
        (MainPageLocators.FUTURE_OF_INTERNET_LOCATOR,
         "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"),
        (MainPageLocators.LETS_TALK_ABOUT_SMTP_LOCATOR,
         "https://ru.wikipedia.org/wiki/SMTP")
    ])
    def test_go_to_page(self, link, expected_url):
        self.login_page.login(username=self.user.username, password=self.user.password)

        self.main_page.go_to_page(link)

        assert self.driver.current_url == expected_url

    @allure.description('Проверка перехода по ссылкам в навигационной панели')
    @pytest.mark.parametrize("name, link, expected_url", [
        (MainPageLocators.PYTHON_LOCATOR,
         MainPageLocators.LINK_PYTHON_HISTORY_LOCATOR,
         "https://en.wikipedia.org/wiki/History_of_Python"),
        (MainPageLocators.PYTHON_LOCATOR,
         MainPageLocators.LINK_ABOUT_FLASK_LOCATOR,
         "https://flask.palletsprojects.com/en/1.1.x/#"),
        (MainPageLocators.LINUX_LOCATOR,
         MainPageLocators.LINK_DOWNLOAD_CENTOS7_LOCATOR,
         "https://getfedora.org/ru/workstation/download/"),
        (MainPageLocators.NETWORK_LOCATOR,
         MainPageLocators.LINK_NEWS_LOCATOR,
         "https://www.wireshark.org/news/"),
        (MainPageLocators.NETWORK_LOCATOR,
         MainPageLocators.LINK_DOWNLOAD_LOCATOR,
         "https://www.wireshark.org/#download"),
        (MainPageLocators.NETWORK_LOCATOR,
         MainPageLocators.LINK_EXAMPLES_LOCATOR,
         "https://hackertarget.com/tcpdump-examples/")
    ])
    def test_go_to_page_in_navbar(self, name, link, expected_url):
        self.login_page.login(username=self.user.username, password=self.user.password)

        self.main_page.go_to_page_in_navbar(name, link)

        assert self.driver.current_url == expected_url
