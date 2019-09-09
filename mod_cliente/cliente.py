# coding: utf-8
from flask import Blueprint, render_template

bp_cliente = Blueprint('cliente', __name__, url_prefix='/', template_folder='templates')


@bp_cliente.route("/clientes")
def lista():
    return render_template("formListaClientes.html"), 200


@bp_cliente.route("/cliente")
@bp_cliente.route("/cliente/<int:clienteid>")
def formulario(clienteid=None):
    if clienteid is not None:
        add = True  # Cadastro de novo cliente
    else:
        add = False  # Editar cliente
    return render_template("formCliente.html"), 200
