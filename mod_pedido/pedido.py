# coding: utf-8
from flask import Blueprint, render_template

bp_pedido = Blueprint('pedido', __name__, url_prefix='/', template_folder='templates')


@bp_pedido.route("/pedidos")
def lista():
    return render_template("formListaPedidos.html"), 200


@bp_pedido.route("/pedido")
@bp_pedido.route("/pedido/<int:pedidoid>")
def formulario(pedidoid=None):
    if pedidoid is not None:
        add = True  # Cadastro de novo pedido
    else:
        add = False  # Editar pedido
    return render_template("formPedido.html"), 200
