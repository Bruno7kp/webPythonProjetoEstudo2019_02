from typing import List
from model.base import BaseModel


class ProdutoModel(BaseModel):
    def __init__(self, id_produto=0, descricao="", valor=0, imagem=""):
        super().__init__()
        self.id_produto = id_produto
        self.descricao = descricao
        self.valor = valor
        self.imagem = imagem

    def serialize(self):
        return {
            'id_produto': self.id_produto,
            'descricao': self.descricao,
            'valor': self.valor,
            'imagem': self.imagem,
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
        c.execute("""SELECT id_produto, descricao, valor, imagem FROM tb_produtos WHERE id_produto = %s""", id_produto)
        for row in c:
            self.id_produto = row[0]
            self.descricao = row[1]
            self.valor = row[2]
            self.imagem = row[3]
        c.close()
        return self

    def all(self):
        c = self.db.con.cursor()
        c.execute("""SELECT id_produto, descricao, valor, imagem FROM tb_produtos ORDER BY descricao""")
        list_all: List[ProdutoModel] = []
        for (row, key) in c:
            list_all[key] = ProdutoModel()
            list_all[key].id_produto = row[0]
            list_all[key].descricao = row[1]
            list_all[key].valor = row[2]
            list_all[key].imagem = row[3]
        c.close()
        return list_all
