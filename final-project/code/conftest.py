import logging
import os
import shutil
import sys
import pytest

from mysql.builder import MySQLBuilder
from mysql.client import MySQLClient


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests\\vk_final_project'
    else:
        base_dir = '/tmp/tests/vk_final_project'

    mysql_client = MySQLClient(user='test_qa', password='qa_test', db_name='vkeducation', host='127.0.0.1', port=3306)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
        mysql_client.connect(db_created=True)
        mysql_client.create_table(table_name="test_users")
        mysql_client.connection.close()

        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.mysql_client = mysql_client

    config.base_temp_dir = base_dir


@pytest.fixture(scope='session')
def mysql_client(request) -> MySQLClient:
    # client = MySQLClient(user='test_qa', password='qa_test', db_name='vkeducation', host='127.0.0.1', port=3306)
    client = request.config.mysql_client
    client.connect()
    yield client
    client.connection.close()


# фиктура по созданию и удалению пользователя
@pytest.fixture(scope='function')
def mysql_builder(mysql_client) -> MySQLBuilder:
    new_user = MySQLBuilder(mysql_client)
    yield new_user
    new_user.delete_user()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


# @pytest.fixture(scope='session')
# def base_temp_dir():
#     if sys.platform.startswith('win'):
#         base_dir = 'C:\\tests\\vk_final_project'
#     else:
#         base_dir = '/tmp/tests/vk_final_project'
#     if os.path.exists(base_dir):
#         shutil.rmtree(base_dir)
#     return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    if sys.platform.startswith('win'):
        test_dir = "".join((test_dir[:2], test_dir[2:].replace(':', "_")))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

