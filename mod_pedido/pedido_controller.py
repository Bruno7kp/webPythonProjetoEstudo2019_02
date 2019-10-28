# coding: utf-8
from flask import Blueprint, render_template
from mod_login.login_controller import logado

bp_pedido = Blueprint('pedido', __name__, url_prefix='/', template_folder='templates')


@bp_pedido.route("/pedidos")
@logado
def lista():
    return render_template("lista_pedido.html")


@bp_pedido.route("/pedido")
@bp_pedido.route("/pedido/<int:pedidoid>")
@logado
def formulario(pedidoid=None):
    if pedidoid is not None:
        add = True  # Cadastro de novo pedido
    else:
        add = False  # Editar pedido
    return render_template("form_pedido.html")
