from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME_LOCATOR = (By.ID, 'username')
    PASSWORD_LOCATOR = (By.ID, 'password')
    LOGIN_BUTTON_LOCATOR = (By.ID, 'submit')
    ERROR_LOGIN_MESSAGE_LOCATOR = (By.ID, 'flash')
    GO_TO_REGISTRATION_PAGE_LOCATOR = (By.XPATH, '//a[@href="/reg"]')


class MainPageLocators:
    LOGO_LOCATOR = (By.ID, '//ul/a[@href= "/"]')
    HOME_LOCATOR = (By.XPATH, '//a[text() = "HOME"]')

    PYTHON_LOCATOR = (By.XPATH, '//a[@href = "https://www.python.org/"]')
    LINK_PYTHON_HISTORY_LOCATOR = (By.XPATH, '//a[@href = "https://en.wikipedia.org/wiki/History_of_Python"]')
    LINK_ABOUT_FLASK_LOCATOR = (By.XPATH, '//a[@href = "https://flask.palletsprojects.com/en/1.1.x/#"]')

    LINUX_LOCATOR = (By.XPATH, '//a[text() = "Linux"]')
    LINK_DOWNLOAD_CENTOS7_LOCATOR = (By.XPATH, '//a[@href = "https://getfedora.org/ru/workstation/download/"]')

    NETWORK_LOCATOR = (By.XPATH, '//a[text() = "Network"]')
    LINK_NEWS_LOCATOR = (By.XPATH, '//a[@href = "https://www.wireshark.org/news/"]')
    LINK_DOWNLOAD_LOCATOR = (By.XPATH, '//a[@href = "https://www.wireshark.org/#download"]')
    LINK_EXAMPLES_LOCATOR = (By.XPATH, '//a[@href = "https://hackertarget.com/tcpdump-examples/"]')

    LOGOUT_LOCATOR = (By.XPATH, '//a[@href="/logout"]')

    WHAT_IS_AN_API_LOCATOR = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    FUTURE_OF_INTERNET_LOCATOR = (By.XPATH,
        '//a[@href="https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"]')
    LETS_TALK_ABOUT_SMTP_LOCATOR = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')

    USERNAME_LOCATOR = (By.XPATH, '//div[@id="login-name"]//li[1]')
    NAME_SURNAME_LOCATOR = (By.XPATH, '//div[@id="login-name"]//li[2]')
    VK_ID_LOCATOR = (By.XPATH, '//div[@id="login-name"]//li[3]')


class RegistrationPageLocators:
    NAME_LOCATOR = (By.ID, 'user_name')
    SURNAME_LOCATOR = (By.ID, 'user_surname')
    MIDDLE_NAME_LOCATOR = (By.ID, 'user_middle_name')
    USERNAME_LOCATOR = (By.ID, 'username')
    EMAIL_LOCATOR = (By.ID, 'email')
    PASSWORD_LOCATOR = (By.ID, 'password')
    REPEAT_PASSWORD = (By.ID, 'confirm')
    ACCEPT_CHECKBOX_LOCATOR = (By.ID, 'term')
    REGISTER_BUTTON_LOCATOR = (By.ID, 'submit')
    ERROR_REGISTER_MESSAGE_LOCATOR = (By.ID, 'flash')

