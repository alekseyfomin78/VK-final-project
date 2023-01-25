from urllib.parse import urljoin

import allure
import requests


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=False, params=None,
                 json=None):

        url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params, json=json)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')

        if jsonify:
            return response.json()

        return response

    @allure.step('Post registration user')
    def post_registration_user(self, name=None, surname=None, middle_name=None, username=None, email=None,
                               password=None, expected_status=201):
        location = '/api/user'

        headers = {"Content-Type": "application/json"}

        data = {
            'name': name,
            'surname': surname,
            'middle_name': middle_name,
            'username': username,
            'email': email,
            'password': password,
        }

        return self._request(method='POST', location=location, headers=headers, data=data, expected_status=expected_status)

    @allure.step('Delete user')
    def delete_user(self, username, expected_status=204):
        location = f'/api/user/{username}'

        return self._request(method='DELETE', location=location, expected_status=expected_status)

    @allure.step('Update password')
    def put_update_password(self, username, password, expected_status=200):
        location = f'/api/user/{username}/change-password'

        headers = {"Content-Type": "application/json"}

        data = {
            "password": password,
        }

        return self._request(method='PUT', location=location, headers=headers, data=data, expected_status=expected_status)

    @allure.step('Block user')
    def post_user_block(self, username, expected_status=200):
        location = f'/api/user/{username}/block'

        return self._request(method='POST', location=location, expected_status=expected_status)

    @allure.step('Unblock user')
    def post_user_accept(self, username, expected_status=200):
        location = f'/api/user/{username}/accept'

        return self._request(method='POST', location=location, expected_status=expected_status)

    @allure.step('Get app status')
    def get_app_status(self, expected_status=200):
        location = '/status'

        return self._request(method='GET', location=location, expected_status=expected_status)

    @allure.step('Login')
    def post_login(self, username=None, password=None, expected_status=200):
        location = '/login'

        data = {
            'username': username,
            'password': password,
        }

        return self._request(method='POST', location=location, data=data, expected_status=expected_status)

    @allure.step('Logout')
    def get_logout(self, expected_status=200):
        location = '/logout'

        return self._request(method='GET', location=location, expected_status=expected_status)

