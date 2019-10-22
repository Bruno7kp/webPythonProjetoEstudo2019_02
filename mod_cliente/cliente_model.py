from typing import List
import bcrypt
from model.base import BaseModel


class ClienteModel(BaseModel):
    def __init__(self, id_cliente=0, nome="", endereco="", numero=0, observacao="", cep="", bairro="", cidade="",
                 estado="", telefone="", email="", login="", senha="", grupo=""):
        super().__init__()
        self.id_cliente = id_cliente
        self.nome = nome
        self.endereco = endereco
        self.numero = numero
        self.observacao = observacao
        self.cep = cep
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone
        self.email = email
        self.login = login
        self.senha = senha
        self.grupo = grupo

    def serialize(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'endereco': self.endereco,
            'numero': self.numero,
            'observacao': self.observacao,
            'cep': self.cep,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'telefone': self.telefone,
            'email': self.email,
            'login': self.login,
            'grupo': self.grupo,
            'grupo_name': ClienteModel.get_group_name(self.grupo)
        }

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO tb_clientes (nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            self.nome, self.endereco, self.numero, self.observacao, self.cep, self.bairro, self.cidade, self.estado,
            self.telefone, self.email, self.login, self.senha, self.grupo))
        self.db.con.commit()
        self.id_cliente = c.lastrowid
        c.close()
        return self.id_cliente

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE tb_clientes SET nome = %s, endereco = %s, numero = %s, observacao = %s, cep = %s,
         bairro = %s, cidade = %s, estado = %s, telefone = %s, email = %s, login = %s, senha = %s, grupo = %s 
         WHERE id_cliente = %s""", (self.nome, self.endereco, self.numero, self.observacao, self.cep, self.bairro,
                                    self.cidade, self.estado, self.telefone, self.email, self.login, self.senha,
                                    self.grupo, self.id_cliente))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM tb_clientes WHERE id_cliente = %s""", self.id_cliente)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, id_cliente):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente, nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo FROM tb_clientes WHERE id_cliente = %s""", id_cliente)
        for row in c:
            self.populate_from_db(row)
        c.close()
        return self

    def select_by_login(self, login):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente, nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo FROM tb_clientes WHERE login = %s""", login)
        for row in c:
            self.populate_from_db(row)
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente, nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo FROM tb_clientes ORDER BY nome""")
        list_all: List[ClienteModel] = []
        for row in c:
            cliente = ClienteModel()
            cliente.populate_from_db(row)
            list_all.append(cliente)
        c.close()
        return list_all

    def populate_from_db(self, row):
        self.id_cliente = row[0]
        self.nome = row[1]
        self.endereco = row[2]
        self.numero = row[3]
        self.observacao = row[4]
        self.cep = row[5]
        self.bairro = row[6]
        self.cidade = row[7]
        self.estado = row[8]
        self.telefone = row[9]
        self.email = row[10]
        self.login = row[11]
        self.senha = row[12]
        self.grupo = row[13]

    def login_exists(self, login, exceptid):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente FROM tb_clientes WHERE id_cliente != %s AND login = %s""", (exceptid, login))
        rows = c.rowcount
        c.close()
        return rows > 0

    @staticmethod
    def get_group_name(group: str):
        if group == 'user':
            return 'Cliente'
        elif group == 'admin':
            return 'Administrador'
        return ''

    @staticmethod
    def valid_pass(password):
        return len(password) >= 4

    @staticmethod
    def hash(password):
        return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_hash(password, hashed):
        return bcrypt.checkpw(bytes(password, encoding='utf-8'), bytes(hashed, encoding='utf-8'))
