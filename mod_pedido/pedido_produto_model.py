from typing import List
from model.base import BaseModel


class PedidoProdutoModel(BaseModel):
    def __init__(self, id_pedido=0, id_produto=0, quantidade=0, valor=0, observacao=""):
        super().__init__()
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.valor = valor
        self.observacao = observacao

    def serialize(self):
        return {
            'id_pedido': self.id_pedido,
            'id_produto': self.id_produto,
            'quantidade': self.quantidade,
            'valor': self.valor,
            'observacao': self.observacao,
        }

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO tb_pedido_produtos (id_pedido, id_produto, quantidade, valor, observacao) 
        VALUES (%s, %s, %s, %s, %s)""", (self.id_pedido, self.id_produto, self.quantidade, self.valor, self.observacao))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE tb_pedido_produtos SET quantidade = %s, valor = %s, observacao = %s 
        WHERE id_pedido = %s AND id_produto = %s""", (
            self.quantidade, self.valor, self.observacao, self.id_pedido, self.id_produto))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM tb_pedido_produtos WHERE id_pedido = %s AND id_produto = %s""", (
            self.id_pedido, self.id_produto))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, id_pedido):
        """Seleciona todos os produtos do pedido"""
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, id_produto, quantidade, valor, observacao 
                FROM tb_pedido_produtos WHERE id_pedido = %s""", id_pedido)
        list_all: List[PedidoProdutoModel] = []
        for (row, key) in c:
            list_all[key] = PedidoProdutoModel()
            list_all[key].id_pedido = row[0]
            list_all[key].id_produto = row[1]
            list_all[key].quantidade = row[2]
            list_all[key].valor = row[3]
            list_all[key].observacao = row[4]
        c.close()
        return list_all

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, id_produto, quantidade, valor, observacao 
        FROM tb_pedido_produtos ORDER BY id_pedido DESC""")
        list_all: List[PedidoProdutoModel] = []
        for (row, key) in c:
            list_all[key] = PedidoProdutoModel()
            list_all[key].id_pedido = row[0]
            list_all[key].id_produto = row[1]
            list_all[key].quantidade = row[2]
            list_all[key].valor = row[3]
            list_all[key].observacao = row[4]
        c.close()
        return list_all
