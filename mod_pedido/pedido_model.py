from typing import List
from model import BaseModel


class Pedido(BaseModel):
    def __init__(self, id_pedido=0, data_hora="", id_cliente=0, observacao=""):
        super().__init__()
        self.id_pedido = id_pedido
        self.data_hora = data_hora
        self.id_cliente = id_cliente
        self.observacao = observacao

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO tb_pedidos (data_hora, id_cliente, observacao) VALUES (%s, %s, %s)""", (
            self.data_hora, self.id_cliente, self.observacao))
        self.db.con.commit()
        self.id_pedido = c.lastrowid
        c.close()
        return self.id_pedido

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE tb_pedidos SET data_hora = %s, id_cliente = %s, observacao = %s WHERE id_cliente = %s""", (
            self.data_hora, self.id_cliente, self.observacao, self.id_pedido))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM tb_pedidos WHERE id_pedido = %s""", self.id_pedido)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, id_pedido):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, data_hora, id_cliente, observacao FROM tb_pedidos WHERE id_pedido = %s""", id_pedido)
        for row in c:
            self.id_pedido = row[0]
            self.data_hora = row[1]
            self.id_cliente = row[2]
            self.observacao = row[3]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, data_hora, id_cliente, observacao FROM tb_pedidos ORDER BY id_pedido DESC""")
        list_all: List[Pedido] = []
        for (row, key) in c:
            list_all[key] = Pedido()
            list_all[key].id_pedido = row[0]
            list_all[key].data_hora = row[1]
            list_all[key].id_cliente = row[2]
            list_all[key].observacao = row[3]
        c.close()
        return list_all
