from decimal import Decimal
from typing import List
from mod_base.base import BaseModel


class Produto(BaseModel):
    def __init__(self, id_produto=0, descricao="", valor=0, imagem=""):
        super().__init__()
        self.id_produto = id_produto
        self.descricao = descricao
        self.valor = valor
        self.imagem = imagem

    def serialize(self):
        imagem = self.imagem
        if isinstance(imagem, bytes):
            imagem = imagem.decode("utf-8")
        valor = self.valor
        if isinstance(valor, Decimal):
            valor = str(valor)
        return {
            'id_produto': self.id_produto,
            'descricao': self.descricao,
            'valor': valor,
            'imagem': imagem,
        }

    def insert(self) -> int:
        c = self.db.con.cursor()
        c.execute("""INSERT INTO tb_produtos (descricao, valor, imagem) VALUES (%s, %s, %s)""", (
            self.descricao, self.valor, self.imagem))
        self.db.con.commit()
        self.id_produto = c.lastrowid
        c.close()
        return self.id_produto

    def update(self) -> int:
        c = self.db.con.cursor()
        c.execute("""UPDATE tb_produtos SET descricao = %s, valor = %s, imagem = %s WHERE id_produto = %s""", (
            self.descricao, self.valor, self.imagem, self.id_produto))
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def delete(self) -> int:
        c = self.db.con.cursor()
        c.execute("""DELETE FROM tb_produtos WHERE id_produto = %s""", self.id_produto)
        self.db.con.commit()
        rows = c.rowcount
        c.close()
        return rows

    def select(self, id_produto):
        c = self.db.con.cursor()
        c.execute("""SELECT id_produto, descricao, valor, imagem FROM tb_produtos WHERE id_produto = %s ORDER BY 
        descricao""", id_produto)
        for row in c:
            self.id_produto = row[0]
            self.descricao = row[1]
            self.valor = row[2]
            self.imagem = row[3]
        c.close()
        return self

    def bought(self):
        c = self.db.con.cursor()
        c.execute("SELECT id_produto FROM tb_pedido_produtos WHERE id_produto = %s", self.id_produto)
        c.close()
        return c.rowcount > 0

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_produto, descricao, valor, imagem FROM tb_produtos ORDER BY descricao""")
        list_all: List[Produto] = []
        for row in c:
            produto = Produto()
            produto.id_produto = row[0]
            produto.descricao = row[1]
            produto.valor = row[2]
            produto.imagem = row[3]
            list_all.append(produto)
        c.close()
        return list_all
