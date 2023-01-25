import pytest
import os
import allure
from ui.pages.login_page import LoginPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage
from mysql.client import MySQLClient
from mysql.builder import MySQLBuilder, Builder, User


class UIBase:
    driver = None
    create_user_in_db = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request, mysql_client, mysql_builder):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.mysql_client: MySQLClient = mysql_client
        self.user: User = Builder.create_user()
        self.builder: MySQLBuilder = mysql_builder

        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

        if self.create_user_in_db:
            self.builder.create_user(
                username=self.user.username,
                name=self.user.name,
                surname=self.user.surname,
                middle_name=self.user.middle_name,
                password=self.user.password,
                email=self.user.email
            )

    def get_all_from_table(self, model, **filters):
        self.mysql_client.session.commit()
        res = self.mysql_client.session.query(model).filter_by(**filters)
        return res.all()

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, temp_dir):
        yield
        browser_logs = os.path.join(temp_dir, 'browser.log')
        with open(browser_logs, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")

        with open(browser_logs, 'r') as f:
            allure.attach(f.read(), 'browser.log', allure.attachment_type.TEXT)

        allure.attach.file(os.path.join(temp_dir, 'test.log'), 'test.log', allure.attachment_type.TEXT)

        screenshot_path = os.path.join(temp_dir, 'screenshot.png')
        driver.get_screenshot_as_file(screenshot_path)
        allure.attach.file(screenshot_path, 'screenshot.png', allure.attachment_type.PNG)
