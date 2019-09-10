# coding: utf-8
from flask import Blueprint, render_template
from mod_login.login import logado

bp_produto = Blueprint('produto', __name__, url_prefix='/', template_folder='templates')


@bp_produto.route("/produtos")
@logado
def lista():
    return render_template("formListaProdutos.html")


@bp_produto.route("/produto")
@bp_produto.route("/produto/<int:produtoid>")
@logado
def formulario(produtoid=None):
    if produtoid is not None:
        add = True  # Cadastro de novo produto
    else:
        add = False  # Editar produto
    return render_template("formProduto.html")
