import pytest
import allure
from base import BaseApi
from mysql.model import TestUsers


class TestAppStatus(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Status app')
    @allure.description('Проверка статус кода приложения')
    def test_app_status(self):
        self.api_client.get_app_status(expected_status=200)


class TestRegistrationPositive(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя с middle_name')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 201")
    def test_registration_user(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            expected_status=201,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username, middle_name=self.user.middle_name)

        assert len(reg_user) == 1

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без middle_name')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 201")
    def test_registration_user_without_middle_name(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            expected_status=201,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username, middle_name=None)

        assert len(reg_user) == 1


class TestRegistrationNegative(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя, когда данный пользователь уже существует')
    @pytest.mark.xfail(reason="Статус код ответа 500, ожидается 304")
    def test_user_already_exists(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email)

        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            expected_status=304,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(reg_user) == 1

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без name')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_registration_user_without_name(self):
        self.api_client.post_registration_user(
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            expected_status=400,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(reg_user) == 0

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без surname')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_registration_user_without_surname(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
            expected_status=400,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(reg_user) == 0

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без username')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_registration_user_without_username(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            email=self.user.email,
            password=self.user.password,
            expected_status=400,
        )

        reg_user = self.get_all_from_table(model=TestUsers, email=self.user.email)

        assert len(reg_user) == 0

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без email')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_registration_user_without_email(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            password=self.user.password,
            expected_status=400,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(reg_user) == 0

    @allure.epic('API tests')
    @allure.feature('Registration')
    @allure.description('Проверка регистрации пользователя без password')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_registration_user_without_password(self):
        self.api_client.post_registration_user(
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            username=self.user.username,
            email=self.user.email,
            expected_status=400,
        )

        reg_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(reg_user) == 0


class TestLoginPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Login')
    @allure.description('Проверка логина пользователя с корректными данными')
    def test_correct_credentials(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        login_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=1)

        assert len(login_user) == 1


class TestLoginNegative(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Login')
    @allure.description('Проверка логина пользователя, когда этот пользователь не зарегистрирован')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 404")
    def test_user_not_created(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=404)

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(user_in_db) == 0

    @allure.epic('API tests')
    @allure.feature('Login')
    @allure.description('Проверка логина пользователя с несовпадающим username')
    def test_incorrect_username(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email,
        )

        self.api_client.post_login(username='some_username', password=self.user.password, expected_status=401)

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(user_in_db) == 1

    @allure.epic('API tests')
    @allure.feature('Login')
    @allure.description('Проверка логина пользователя с несовпадающим password')
    def test_incorrect_password(self):
        self.builder.create_user(
            username=self.user.username,
            name=self.user.name,
            surname=self.user.surname,
            middle_name=self.user.middle_name,
            password=self.user.password,
            email=self.user.email,
        )

        self.api_client.post_login(username=self.user.username, password='some_password', expected_status=401)

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(user_in_db) == 1


class TestDeleteUserPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Delete user')
    @allure.description('Проверка удаления существующего пользователя')
    def test_delete_user(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.delete_user(username=self.user.username, expected_status=204)

        deleted_user = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(deleted_user) == 0


class TestDeleteUserNegative(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Delete user')
    @allure.description('Проверка удаления несуществующего пользователя')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 404")
    def test_delete_non_existent_user(self):
        self.api_client.delete_user(username=self.user.username, expected_status=404)

        user_in_db = self.get_all_from_table(model=TestUsers, username=self.user.username)

        assert len(user_in_db) == 0


class TestUpdatePasswordPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Update user')
    @allure.description('Проверка обновления пароля у существующего пользователя')
    @pytest.mark.xfail(reason="Статус код ответа 500, ожидается 200")
    def test_update_password(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.put_update_password(username=self.user.username, password='new_password', expected_status=200)

        updated_user = self.get_all_from_table(model=TestUsers, username=self.user.username, password='new_password')

        assert len(updated_user) == 1


class TestUpdatePasswordNegative(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Update user')
    @allure.description('Проверка обновления пароля, который совпадает со старым паролем, у существующего пользователя')
    @pytest.mark.xfail(reason="Статус код ответа 500, ожидается 400")
    def test_update_password_similar_to_old_password(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.put_update_password(username=self.user.username, password=self.user.password, expected_status=400)


class TestUserBlockPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Block user')
    @allure.description('Проверка блокировки существующего пользователя')
    def test_user_block(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.post_user_block(username=self.user.username, expected_status=200)

        blocked_user = self.get_all_from_table(model=TestUsers, username=self.user.username, access=0)

        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=401)

        assert len(blocked_user) == 1


class TestUserBlockNegative(BaseApi):
    create_user_in_db = False

    @allure.epic('API tests')
    @allure.feature('Block user')
    @allure.description('Проверка блокировки несуществующего пользователя')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 400")
    def test_block_non_existent_user(self):
        self.api_client.post_user_block(username=self.user.username, expected_status=400)


class TestUserUnblockPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Unblock user')
    @allure.description('Проверка разблокировки заблокированного пользователя')
    @pytest.mark.xfail(reason="Статус код ответа 401, ожидается 200")
    def test_user_unblock(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.post_user_block(username=self.user.username, expected_status=200)

        blocked_user = self.get_all_from_table(model=TestUsers, username=self.user.username, access=0)

        assert len(blocked_user) == 1

        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=401)

        self.api_client.post_user_accept(username=self.user.username, expected_status=200)

        unblocked_user = self.get_all_from_table(model=TestUsers, username=self.user.username, access=1)

        assert len(unblocked_user) == 1


class TestUserUnblockNegative(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Unblock user')
    @allure.description('Проверка разблокировки незаблокированного пользователя')
    def test_unblock_an_unblocked_user(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        self.api_client.post_user_accept(username=self.user.username, expected_status=400)

        unblocked_user = self.get_all_from_table(model=TestUsers, username=self.user.username, access=1)

        assert len(unblocked_user) == 1


class TestLogoutPositive(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Logout')
    @allure.description('Проверка выхода пользователя из приложения')
    def test_logout(self):
        self.api_client.post_login(username=self.user.username, password=self.user.password, expected_status=200)

        authorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=1)

        assert len(authorized_user) == 1

        self.api_client.get_logout(expected_status=200)

        unauthorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(unauthorized_user) == 1


class TestLogoutNegative(BaseApi):
    create_user_in_db = True

    @allure.epic('API tests')
    @allure.feature('Logout')
    @allure.description('Проверка выхода пользователя, который не был залогинен, из приложения')
    @pytest.mark.xfail(reason="Статус код ответа 200, ожидается 400")
    def test_logout_of_a_user_not_logged_in(self):
        self.api_client.get_logout(expected_status=400)

        unauthorized_user = self.get_all_from_table(model=TestUsers, username=self.user.username, active=0)

        assert len(unauthorized_user) == 0
