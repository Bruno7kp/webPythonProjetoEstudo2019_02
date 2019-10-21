from typing import List
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

    def select(self, id_produto):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente, nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo FROM tb_clientes WHERE id_cliente = %s""", id_produto)
        for row in c:
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
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_cliente, nome, endereco, numero, observacao, cep, bairro, cidade, estado, telefone,
         email, login, senha, grupo FROM tb_clientes ORDER BY nome""")
        list_all: List[ClienteModel] = []
        for (row, key) in c:
            list_all[key] = ClienteModel()
            list_all[key].id_cliente = row[0]
            list_all[key].nome = row[1]
            list_all[key].endereco = row[2]
            list_all[key].numero = row[3]
            list_all[key].observacao = row[4]
            list_all[key].cep = row[5]
            list_all[key].bairro = row[6]
            list_all[key].cidade = row[7]
            list_all[key].estado = row[8]
            list_all[key].telefone = row[9]
            list_all[key].email = row[10]
            list_all[key].login = row[11]
            list_all[key].senha = row[12]
            list_all[key].grupo = row[13]
        c.close()
        return list_all
