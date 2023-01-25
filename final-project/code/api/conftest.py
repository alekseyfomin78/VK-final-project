import pytest
from api.client.client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--url', default='http://127.0.0.1:8086')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')

    return {
        'url': url,
        'debug_log': debug_log,
    }


@pytest.fixture(scope='session')
def api_client(config) -> ApiClient:
    api_client = ApiClient(config['url'])
    return api_client
