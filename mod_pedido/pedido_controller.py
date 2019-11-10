# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for

from mod_cliente.cliente_model import Cliente
from mod_login.login_controller import logado
from mod_pedido.pedido_model import Pedido
from mod_produto.produto_model import Produto

bp_pedido = Blueprint('pedido', __name__, url_prefix='/', template_folder='templates')


@bp_pedido.route('/pedidos')
@logado
def lista():
    return render_template('lista_pedido.html')


@bp_pedido.route('/pedido', methods=['GET'])
@logado
def cadastro_form():
    # Página de cadastro
    pedido = Pedido()
    cliente = Cliente()
    clientes = cliente.all()
    produto = Produto()
    produtos = produto.all()
    return render_template('form_pedido.html', pedido=pedido, clientes=clientes, produtos=produtos)


@bp_pedido.route('/pedido/<int:pedidoid>')
@logado
def edicao_form(pedidoid: int):
    # Página de edição
    pedido = Pedido()
    pedido.select(pedidoid)
    if pedido.id_pedido == 0:
        return redirect(url_for('pedido.lista'))
    cliente = Cliente()
    clientes = cliente.all()
    produto = Produto()
    produtos = produto.all()
    return render_template('form_pedido.html', pedido=pedido, clientes=clientes, produtos=produtos)
