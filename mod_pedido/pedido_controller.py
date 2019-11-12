# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for, request, make_response

from mod_base.json_response import json_response
from mod_cliente.cliente_model import Cliente
from mod_login.login_controller import logado
from mod_pedido.pedido_model import Pedido, PedidoProduto
from mod_produto.produto_model import Produto

bp_pedido = Blueprint('pedido', __name__, url_prefix='/', template_folder='templates')


@bp_pedido.route('/pedidos')
@logado
def lista():
    pedido = Pedido()
    pedidos = pedido.all()
    return render_template('lista_pedido.html', pedidos=pedidos)


@bp_pedido.route('/pedido', methods=['GET'])
@logado
def cadastro_form():
    # Página de cadastro
    pedido = Pedido()
    pedido.produtos.append(PedidoProduto())
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


@bp_pedido.route('/pedido', methods=['POST'])
@logado
def cadastro():
    # Cadastro via ajax
    pedido = Pedido()
    populate_from_request(pedido)

    identifier = pedido.insert()
    if identifier > 0:
        return json_response(message='Pedido cadastrado!', data=[pedido], redirect=url_for('pedido.lista')), 201
    else:
        return json_response(message='Não foi possível cadastrar o pedido', data=[]), 400


@bp_pedido.route('/pedido/<int:pedidoid>', methods=['POST', 'PUT'])
@logado
def edicao(pedidoid):
    # Edição via ajax
    # Verifica se pedido existe
    pedido = Pedido()
    pedido.select(pedidoid)
    if pedido.id_pedido == 0:
        return json_response(message='Pedido não encontrado!', data=[], redirect=url_for('pedido.lista')), 404

    populate_from_request(pedido)

    rows = pedido.update()
    if rows > 0:
        return json_response(message='Pedido atualizado!', data=[pedido]), 200
    else:
        return json_response(message='Não foi possível editar o pedido', data=[]), 400


@bp_pedido.route('/pedido/download/<int:pedidoid>', methods=['GET'])
@logado
def download(pedidoid):
    # Download do pdf
    # Verifica se pedido existe
    pedido = Pedido()
    pedido.select(pedidoid)
    if pedido.id_pedido == 0:
        return json_response(message='Pedido não encontrado!', data=[]), 404
    pdf = pedido.create_pdf()
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='pedido' + pedido.id_pedido.__str__() + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response


def populate_from_request(pedido: Pedido):
    # Atribui valores do post ao model
    pedido.id_cliente = request.form['id_cliente']
    pedido.observacao = request.form['observacao']
    pedido.data_hora = request.form['data_hora']
    pedido.produtos = []
    dicti = request.form.to_dict(flat=False)
    produtos = []

    key = 0
    for id_produto in dicti['produto[][id_produto]']:
        produtos.append(PedidoProduto())
        produtos[key].id_produto = id_produto
        key = key + 1

    key = 0
    for quantidade in dicti['produto[][quantidade]']:
        produtos[key].quantidade = quantidade
        key = key + 1

    key = 0
    for total in dicti['produto[][total]']:
        produtos[key].valor = total.replace('.', '').replace(',', '.')
        key = key + 1

    key = 0
    for observacao in dicti['produto[][observacao]']:
        produtos[key].observacao = observacao
        key = key + 1

    pedido.produtos = produtos
