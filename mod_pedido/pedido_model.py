from typing import List
from mod_base.base import BaseModel
from mod_cliente.cliente_model import Cliente
from mod_produto.produto_model import Produto


class Pedido(BaseModel):
    def __init__(self, id_pedido=0, data_hora="", id_cliente=0, observacao="", produtos=None, cliente=None):
        super().__init__()
        self.id_pedido = id_pedido
        self.data_hora = data_hora
        self.id_cliente = id_cliente
        self.observacao = observacao
        if produtos is None:
            produtos = []
        self.produtos = produtos
        if cliente is None:
            cliente = Cliente()
        self.cliente = cliente

    def serialize(self):
        return {
            'id_pedido': self.id_pedido,
            'data_hora': self.data_hora,
            'id_cliente': self.id_cliente,
            'observacao': self.observacao,
        }

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO tb_pedidos (data_hora, id_cliente, observacao) VALUES (%s, %s, %s)""", (
            self.data_hora, self.id_cliente, self.observacao))
        self.db.con.commit()
        self.id_pedido = c.lastrowid
        c.close()
        for produto in self.produtos:
            produto.id_pedido = self.id_pedido
            produto.insert()

        return self.id_pedido

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("UPDATE tb_pedidos SET data_hora = %s, id_cliente = %s, observacao = %s WHERE id_cliente = %s", (
            self.data_hora, self.id_cliente, self.observacao, self.id_pedido))
        c.execute("DELETE FROM tb_pedido_produtos WHERE id_pedido = %s", self.id_pedido)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        for produto in self.produtos:
            produto.id_pedido = self.id_pedido
            produto.insert()

        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("DELETE FROM tb_pedidos WHERE id_pedido = %s", self.id_pedido)
        c.execute("DELETE FROM tb_pedido_produtos WHERE id_pedido = %s", self.id_pedido)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, id_pedido):
        c = self.db.con.cursor()
        c.execute("SELECT id_pedido, DATE_FORMAT(data_hora, '%%Y-%%m-%%dT%%H:%%i'), id_cliente, observacao FROM tb_pedidos WHERE id_pedido = %s", id_pedido)
        for row in c:
            self.id_pedido = row[0]
            self.data_hora = row[1]
            self.id_cliente = row[2]
            self.observacao = row[3]
        c.close()
        produto = PedidoProduto()
        self.produtos = produto.select(self.id_pedido)
        cliente = Cliente()
        self.cliente = cliente.select(self.id_cliente)
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, data_hora, id_cliente, observacao FROM tb_pedidos ORDER BY id_pedido DESC""")
        list_all: List[Pedido] = []
        for row in c:
            produto = PedidoProduto()
            cliente = Cliente()
            pedido = Pedido()
            pedido.id_pedido = row[0]
            pedido.data_hora = row[1]
            pedido.id_cliente = row[2]
            pedido.observacao = row[3]
            pedido.produtos = produto.select(pedido.id_pedido)
            pedido.cliente = cliente.select(pedido.id_cliente)
            list_all.append(pedido)
        c.close()
        return list_all


class PedidoProduto(BaseModel):
    def __init__(self, id_pedido=0, id_produto=0, quantidade=0, valor=0, observacao="", produto=None):
        super().__init__()
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.valor = valor
        self.observacao = observacao
        if produto is None:
            produto = Produto()
        self.produto = produto

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
        list_all: List[PedidoProduto] = []
        for row in c:
            prod = Produto()
            produto = PedidoProduto()
            produto.id_pedido = row[0]
            produto.id_produto = row[1]
            produto.quantidade = row[2]
            produto.valor = row[3]
            produto.observacao = row[4]
            produto.produto = prod.select(produto.id_produto)
            list_all.append(produto)
        c.close()
        return list_all

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, id_produto, quantidade, valor, observacao 
        FROM tb_pedido_produtos ORDER BY id_pedido DESC""")
        list_all: List[PedidoProduto] = []
        for (row, key) in c:
            list_all[key] = PedidoProduto()
            list_all[key].id_pedido = row[0]
            list_all[key].id_produto = row[1]
            list_all[key].quantidade = row[2]
            list_all[key].valor = row[3]
            list_all[key].observacao = row[4]
        c.close()
        return list_all
