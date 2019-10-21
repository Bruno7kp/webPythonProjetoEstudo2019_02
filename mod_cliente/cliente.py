# coding: utf-8
from flask import Blueprint, render_template, jsonify, request, make_response
from mod_login.login import logado
from mod_cliente.cliente_model import ClienteModel
import hashlib

bp_cliente = Blueprint('cliente', __name__, url_prefix='/', template_folder='templates')


@bp_cliente.route('/clientes', methods=['GET'])
@logado
def lista():
    return render_template('formListaClientes.html')


@bp_cliente.route('/cliente', methods=['GET'])
@logado
def cadastro_form():
    return render_template('formCliente.html')


@bp_cliente.route('/cliente/<int:clienteid>', methods=['GET'])
@logado
def edicao_form(clienteid: int):
    return render_template('formCliente.html');


@bp_cliente.route('/cliente', methods=['POST'])
@logado
def cadastro():
    cliente = ClienteModel()
    cliente.nome = request.form['nome']
    cliente.endereco = request.form['endereco']
    cliente.numero = request.form['numero']
    cliente.observacao = request.form['observacao']
    cliente.cep = request.form['cep']
    cliente.bairro = request.form['bairro']
    cliente.cidade = request.form['cidade']
    cliente.estado = request.form['estado']
    cliente.telefone = request.form['telefone']
    cliente.email = request.form['email']
    cliente.login = request.form['login']
    cliente.grupo = request.form['grupo']
    cliente.senha = request.form['senha']
    identifier = cliente.insert()
    if identifier > 0:
        return jsonify(cliente), 201
    else:
        return jsonify([]), 500

