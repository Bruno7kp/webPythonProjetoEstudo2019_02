import json

import pymysql
import abc

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "db_abc_bolinhas"


class DataBase:
    def __init__(self):
        self.con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4')


class BaseModel:
    def __init__(self):
        self.db = DataBase()

    @abc.abstractmethod
    def serialize(self):
        return {}

    @abc.abstractmethod
    def insert(self) -> int:
        """Insere de uma linha no banco de dados, retorna o id cadastrado"""
        return 0

    @abc.abstractmethod
    def update(self) -> int:
        """Atualiza uma linha no banco de dados, retorna a quantidade de linhas atualizadas"""
        return 0

    @abc.abstractmethod
    def delete(self) -> int:
        """Remove uma linha no banco de dados, retorna a quantidade de linhas removidas"""
        return 0

    @abc.abstractmethod
    def select(self, identifier):
        """Busca uma linha pelo id"""
        return

    @abc.abstractmethod
    def all(self):
        """Busca todas as linhas do tabela"""
        return
