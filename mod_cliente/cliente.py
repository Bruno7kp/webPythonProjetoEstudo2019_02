# coding: utf-8
from flask import Blueprint, render_template, jsonify, request, make_response, url_for, redirect
from mod_login.login import logado
from mod_cliente.cliente_model import ClienteModel
import hashlib

from model.json_response import json_response

bp_cliente = Blueprint('cliente', __name__, url_prefix='/', template_folder='templates')


@bp_cliente.route('/clientes', methods=['GET'])
@logado
def lista():
    cliente = ClienteModel()
    clientes = cliente.all()
    return render_template('formListaClientes.html', lista=clientes)


@bp_cliente.route('/cliente', methods=['GET'])
@logado
def cadastro_form():
    # Paǵina de cadastro
    cliente = ClienteModel()
    return render_template('formCliente.html', cliente=cliente)


@bp_cliente.route('/cliente/<int:clienteid>', methods=['GET'])
@logado
def edicao_form(clienteid: int):
    # Página de edição
    cliente = ClienteModel()
    cliente.select(clienteid)
    if cliente.id_cliente == 0:
        return redirect(url_for('cliente.lista'))
    return render_template('formCliente.html', cliente=cliente)


@bp_cliente.route('/cliente', methods=['POST'])
@logado
def cadastro():
    # Cadastro via ajax
    cliente = ClienteModel()
    create_from_request(cliente)

    if not cliente.valid_pass(request.form['senha']):
        return json_response(message='A senha deve ter pelo menos 4 dígitos', data=[]), 400

    if cliente.login_exists(cliente.login, 0):
        return json_response(message='O login já está em uso, utilize outro', data=[]), 400

    cliente.senha = request.form['senha']
    identifier = cliente.insert()
    if identifier > 0:
        return json_response(message='Cliente cadastrado!', data=[cliente], redirect=url_for('cliente.lista')), 201
    else:
        return json_response(message='Não foi possível cadastrar o cliente', data=[]), 400


@bp_cliente.route('/cliente/<int:clienteid>', methods=['POST', 'PUT'])
@logado
def edicao(clienteid):
    # Edição via ajax
    # Verifica se usuário existe
    cliente = ClienteModel()
    cliente.select(clienteid)
    if cliente.id_cliente == 0:
        return json_response(message='Cliente não encontrado!', data=[], redirect=url_for('cliente.lista')), 404
    create_from_request(cliente)

    if len(request.form['senha']) > 0:
        if not cliente.valid_pass(request.form['senha']):
            return json_response(message='A senha deve ter pelo menos 4 dígitos', data=[]), 400
        cliente.senha = request.form['senha']

    if cliente.login_exists(cliente.login, cliente.id_cliente):
        return json_response(message='O login já está em uso, utilize outro', data=[]), 400

    rows = cliente.update()
    if rows > 0:
        return json_response(message='Cliente atualizado!', data=[cliente]), 200
    else:
        return json_response(message='Não foi possível editar o cliente', data=[]), 400


@bp_cliente.route('/cliente/<int:clienteid>', methods=['DELETE'])
@logado
def remocao(clienteid):
    # Remoção via ajax
    # Verifica se usuário existe
    cliente = ClienteModel()
    cliente.select(clienteid)
    if cliente.id_cliente == 0:
        return json_response(message='Cliente não encontrado!', data=[], redirect=url_for('cliente.lista')), 404
    rows = cliente.delete()
    if rows > 0:
        return json_response(message='Cliente removido!', data=[cliente], redirect=url_for('cliente.lista')), 200
    else:
        return json_response(message='Não foi possível remover o cliente', data=[]), 400


def create_from_request(cliente: ClienteModel):
    # Atribui valores do post ao model
    cliente.nome = request.form['nome']
    cliente.endereco = request.form['endereco']
    cliente.numero = request.form['numero']
    cliente.observacao = request.form['observacao']
    cliente.cep = ''.join(i for i in request.form['cep'] if i.isdigit())
    cliente.bairro = request.form['bairro']
    cliente.cidade = request.form['cidade']
    cliente.estado = request.form['estado']
    cliente.telefone = ''.join(i for i in request.form['telefone'] if i.isdigit())
    cliente.email = request.form['email']
    cliente.login = request.form['login']
    cliente.grupo = request.form['grupo']
