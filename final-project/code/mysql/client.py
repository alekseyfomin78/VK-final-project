import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from mysql.model import Base, TestUsers


class MySQLClient:

    def __init__(self, user: str, password: str, db_name: str, host: str, port: int):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created: bool = True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table(self, table_name):
        if not inspect(self.engine).has_table(f'{table_name}'):
            Base.metadata.tables[f'{table_name}'].create(self.engine)
