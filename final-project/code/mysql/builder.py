import random
import requests
from mysql.model import TestUsers
from dataclasses import dataclass
import faker

fake = faker.Faker()


@dataclass
class User:
    username: str = None
    name: str = None
    surname: str = None
    middle_name: str = None
    password: str = None
    email: str = None
    access: int = None
    active: int = None


class Builder:
    # создание рандомных данных для пользователя
    @staticmethod
    def create_user(username: str = None, name: str = None, surname: str = None, middle_name: str = None,
                    password: str = None, email: str = None, access: int = 1, active: int = 0) -> User:

        fake_user = fake.simple_profile()

        if username is None:
            username = fake_user['username']
        if name is None:
            name = fake_user['name'].split()[0]
        if surname is None:
            surname = fake_user['name'].split()[-1]
        if middle_name is None:
            middle_name = fake_user['name'].split()[0]
        if password is None:
            password = fake.password()
        if email is None:
            email = fake_user['mail']

        return User(username=username, name=name, surname=surname, middle_name=middle_name, password=password,
                    email=email, access=access, active=active)


class MySQLBuilder:
    def __init__(self, client):
        self.client = client
        self.New_test_user = TestUsers.__table__
        self.new_test_user = None
        self.list_of_all_new_users = []  # список созданных для теста пользователей

    # добавление пользователя в БД
    def create_user(self, username: str, name: str, surname: str, password: str, email: str, access: int = 1,
                    active: int = 0, middle_name: str = None):

        self.new_test_user = TestUsers(
            username=username,
            name=name,
            surname=surname,
            middle_name=middle_name,
            password=password,
            email=email,
            access=access,
            active=active,
        )
        self.client.session.add(self.new_test_user)
        self.client.session.commit()
        self.list_of_all_new_users.append(self.new_test_user)

        # запрос в mock сервер для добавления рандомного vk_id созданному пользователю
        vk_id = str(random.randint(1, 100))
        requests.post(url=f'http://127.0.0.1:5000/vk_id/{self.new_test_user.username}', json={'vk_id': vk_id})

        return self.new_test_user

    def delete_user(self):
        # удаление из БД всех созданных для теста пользователей
        for user in self.list_of_all_new_users:
            self.client.session.delete(user)
        self.client.session.commit()

