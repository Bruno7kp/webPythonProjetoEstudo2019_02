import base64
import io
from typing import List
from urllib.request import urlopen

from fpdf import FPDF, HTMLMixin
from fpdf.php import sprintf, substr

import helper
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
        c.execute("DELETE FROM tb_pedido_produtos WHERE id_pedido = %s", self.id_pedido)
        c.execute("DELETE FROM tb_pedidos WHERE id_pedido = %s", self.id_pedido)
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

    def all_by_cliente_id(self, cliente_id: int):
        c = self.db.con.cursor()
        c.execute("""SELECT id_pedido, data_hora, id_cliente, observacao FROM tb_pedidos WHERE id_cliente = %s 
                    ORDER BY id_pedido DESC""", cliente_id)
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

    def create_pdf(self):
        rows = ""
        c = 1
        for item in self.produtos:
            obs = item.observacao if len(item.observacao) > 0 else "Nenhuma"
            row = "<tr>"
            row = row + "<td width='5%' align='center'>" + c.__str__() + "</td>"
            row = row + "<td width='30%' align='center'>" + item.produto.descricao + "</td>"
            row = row + "<td width='10%' align='center'>R$ " + helper.money(item.produto.valor) + "</td>"
            row = row + "<td width='10%' align='center'>" + item.quantidade.__str__() + "</td>"
            row = row + "<td width='15%' align='center'>R$ " + helper.money(item.valor) + "</td>"
            row = row + "<td width='15%' align='center'>" + obs + "</td>"
            row = row + "<td width='15%'><img height='30' src='" + item.produto.imagem.decode("utf-8") + "'/></td>"
            row = row + "</tr>"
            rows = rows + row
            c = c + 1
        html = """
        <h1 align="center">BoxStore</h1>
        <h2>Pedido #""" + self.id_pedido.__str__() + """</h2>
        <p><small>""" + helper.show_date(self.data_hora.replace("T", " ") + ":00") + """</small></p>
        <br/>
        <h3>Dados do cliente</h3>
        <p><b>Nome:</b> """ + self.cliente.nome + """</p>   
        <p><b>Telefone:</b> """ + helper.telefone(self.cliente.telefone) + """</p>   
        <p><b>E-mail:</b> """ + self.cliente.email + """</p>   
        <p><b>Endereço:</b> """ + self.cliente.endereco + """, """ + self.cliente.numero.__str__() + """. """ + \
               self.cliente.cidade + """ - """ + self.cliente.estado + """</p>   
        <br/>
        <h3>Lista de produtos</h3>  
        <table>
            <thead>
                <tr>
                    <th width="5%">#</th>
                    <th width="30%">Produto</th>
                    <th width="10%">Preço (Uni.)</th>  
                    <th width="10%">Qtd.</th>
                    <th width="15%">Valor total</th>
                    <th width="15%">Observações</th>
                    <th width="15%">Imagem</th>
                </tr>
            </thead>
            <tbody>
                """ + rows + """
            </tbody>
        </table>
        <h3>Observação</h3>
        <p>""" + self.observacao + """</p>
        """

        class MyFPDF(FPDF, HTMLMixin):
            def image(self, name, x=None, y=None, w=0, h=0, type='', link=''):
                "Put an image on the page"
                if not name in self.images:
                    # First use of image, get info
                    if (type == ''):
                        pos = name.rfind('.')
                        if (not pos):
                            self.error('image file has no extension and no type was specified: ' + name)
                        type = substr(name, pos + 1)
                    type = type.lower()
                    if (type == 'jpg' or type == 'jpeg'):
                        info = self._parsejpg(name)
                    elif (name.startswith('data:image/jpeg')):
                        imgdata = name.split('base64,')[1]
                        imgdata = base64.b64decode(imgdata)
                        filename = 'temp_image.jpg'  # I assume you have a way of picking unique filenames
                        with open(filename, 'wb') as f:
                            f.write(imgdata)
                        info = self._parsejpg(filename)
                    elif (name.startswith('data:image/png')):
                        imgdata = name.split('base64,')[1]
                        imgdata = base64.b64decode(imgdata)
                        filename = 'temp_image.png'  # I assume you have a way of picking unique filenames
                        with open(filename, 'wb') as f:
                            f.write(imgdata)
                        info = self._parsepng(filename)
                    elif (type == 'png'):
                        info = self._parsepng(name)
                    else:
                        # Allow for additional formats
                        # maybe the image is not showing the correct extension,
                        # but the header is OK,
                        succeed_parsing = False
                        # try all the parsing functions
                        parsing_functions = [self._parsejpg, self._parsepng, self._parsegif]
                        for pf in parsing_functions:
                            try:
                                info = pf(name)
                                succeed_parsing = True
                                break;
                            except:
                                pass
                        # last resource
                        if not succeed_parsing:
                            mtd = '_parse' + type
                            if not hasattr(self, mtd):
                                self.error('Unsupported 1image type: ' + type)
                            info = getattr(self, mtd)(name)
                        mtd = '_parse' + type
                        if not hasattr(self, mtd):
                            self.error('Unsupported 2image type: ' + type)
                        info = getattr(self, mtd)(name)
                    info['i'] = len(self.images) + 1
                    self.images[name] = info
                else:
                    info = self.images[name]
                # Automatic width and height calculation if needed
                if (w == 0 and h == 0):
                    # Put image at 72 dpi
                    w = info['w'] / self.k
                    h = info['h'] / self.k
                elif (w == 0):
                    w = h * info['w'] / info['h']
                elif (h == 0):
                    h = w * info['h'] / info['w']
                # Flowing mode
                if y is None:
                    if (self.y + h > self.page_break_trigger and not self.in_footer and self.accept_page_break()):
                        # Automatic page break
                        x = self.x
                        self.add_page(self.cur_orientation)
                        self.x = x
                    y = self.y
                    self.y += h
                if x is None:
                    x = self.x
                self._out(sprintf('q %.2f 0 0 %.2f %.2f %.2f cm /I%d Do Q', w * self.k, h * self.k, x * self.k,
                                  (self.h - (y + h)) * self.k, info['i']))
                if (link):
                    self.link(x, y, w, h, link)

            def load_resource(self, reason, filename):
                if reason == "image":
                    if filename.startswith("http://") or filename.startswith("https://"):
                        f = io.BytesIO(urlopen(filename).read())
                    elif filename.startswith("data"):
                        f = filename.split('base64,')[1]
                        f = base64.b64decode(f)
                        f = io.BytesIO(f)
                    else:
                        f = open(filename, "rb")
                    return f
                else:
                    self.error("Unknown resource loading reason \"%s\"" % reason)

        pdf = MyFPDF()
        # First page
        pdf.add_page()
        pdf.write_html(html)
        return pdf


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
