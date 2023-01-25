import pytest
from mysql.client import MySQLClient
from mysql.builder import MySQLBuilder, User, Builder


class BaseApi:
    create_user_in_db = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, config, logger, mysql_client, mysql_builder):
        self.api_client = api_client
        self.config = config
        self.logger = logger
        self.mysql_client: MySQLClient = mysql_client
        self.user: User = Builder.create_user()
        self.builder: MySQLBuilder = mysql_builder

        if self.create_user_in_db:
            self.builder.create_user(
                username=self.user.username,
                name=self.user.name,
                surname=self.user.surname,
                password=self.user.password,
                email=self.user.email,
                middle_name=self.user.middle_name,
            )

    def get_all_from_table(self, model, **filters):
        self.mysql_client.session.commit()
        res = self.mysql_client.session.query(model).filter_by(**filters)
        return res.all()
