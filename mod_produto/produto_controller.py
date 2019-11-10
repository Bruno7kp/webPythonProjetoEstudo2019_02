# coding: utf-8
import base64

from flask import Blueprint, render_template, redirect, url_for, request
from mod_login.login_controller import logado
from mod_produto.produto_model import Produto
from mod_base.json_response import json_response

bp_produto = Blueprint('produto', __name__, url_prefix='/', template_folder='templates')


@bp_produto.route("/produtos", methods=['GET'])
@logado
def lista():
    produto = Produto()
    produtos = produto.all()
    return render_template("lista_produto.html", lista=produtos)


@bp_produto.route("/produto", methods=['GET'])
@logado
def cadastro_form():
    # Página de cadastro
    produto = Produto()
    return render_template("form_produto.html", produto=produto)


@bp_produto.route("/produto/<int:produtoid>", methods=['GET'])
@logado
def edicao_form(produtoid: int):
    # Página de edição
    produto = Produto()
    produto.select(produtoid)
    if produto.id_produto == 0:
        return redirect(url_for('produto.lista'))
    return render_template('form_produto.html', produto=produto)


@bp_produto.route('/cliente', methods=['POST'])
@logado
def cadastro():
    # Cadastro via ajax
    produto = Produto()
    populate_from_request(produto)

    identifier = produto.insert()
    if identifier > 0:
        return json_response(message='Produto cadastrado!', data=[produto], redirect=url_for('produto.lista')), 201
    else:
        return json_response(message='Não foi possível cadastrar o produto', data=[]), 400


@bp_produto.route('/produto/<int:produtoid>', methods=['POST', 'PUT'])
@logado
def edicao(produtoid):
    # Edição via ajax
    # Verifica se usuário existe
    produto = Produto()
    produto.select(produtoid)
    if produto.id_produto == 0:
        return json_response(message='Produto não encontrado!', data=[], redirect=url_for('produto.lista')), 404

    populate_from_request(produto)

    rows = produto.update()
    if rows > 0:
        return json_response(message='Produto atualizado!', data=[produto]), 200
    else:
        return json_response(message='Não foi possível editar o produto', data=[]), 400


@bp_produto.route('/produto/<int:produtoid>', methods=['DELETE'])
@logado
def remocao(produtoid):
    # Remoção via ajax
    # Verifica se usuário existe
    produto = Produto()
    produto.select(produtoid)
    if produto.id_produto == 0:
        return json_response(message='Produto não encontrado!', data=[], redirect=url_for('produto.lista')), 404
    rows = produto.delete()
    if rows > 0:
        return json_response(message='Produto removido!', data=[produto], redirect=url_for('produto.lista')), 200
    else:
        return json_response(message='Não foi possível remover o produto', data=[]), 400


@bp_produto.route('/produto/busca/<int:produtoid>', methods=['GET'])
@logado
def busca(produtoid: int):
    # Busca por produto
    produto = Produto()
    produto.select(produtoid)
    if produto.id_produto == 0:
        return json_response(message='Produto não encontrado!', data=[]), 404
    return json_response(message='Produto encontrado!', data=[produto]), 200



def populate_from_request(produto: Produto):
    # Atribui valores do post ao model
    produto.descricao = request.form['descricao']
    produto.valor = request.form['valor'].replace('.', '').replace(',', '.')
    if 'imagem' in request.files and request.files['imagem'].filename != '':
        produto.imagem = "data:" + request.files['imagem'].content_type + ";base64," + str(
            base64.b64encode(request.files['imagem'].read()), "utf-8")
