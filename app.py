# coding: utf-8
from datetime import timedelta, datetime

from flask import Flask, redirect, url_for
from mod_home.home_controller import bp_home
from mod_pedido.pedido_controller import bp_pedido
from mod_erro.erro_controller import bp_erro
from mod_produto.produto_controller import bp_produto
from mod_cliente.cliente_controller import bp_cliente
from mod_login.login_controller import bp_login, SESSION_LIMIT
import helper

app = Flask(__name__)

app.secret_key = b'_8#y2P"g8l1x\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=SESSION_LIMIT)

app.register_blueprint(bp_home)
app.register_blueprint(bp_pedido)
app.register_blueprint(bp_erro)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_login)


@app.template_filter()
def money(text):
    return helper.money(text)


@app.template_filter()
def cep(text):
    return helper.cep(text)


@app.template_filter()
def telefone(text):
    return helper.telefone(text)


@app.template_filter()
def show_date(text):
    return helper.show_date(text)


@app.context_processor
def inject_user():
    return dict(session_limit=SESSION_LIMIT)


@app.errorhandler(404)
def nao_encontrado(error):
    return redirect(url_for("erro.nao_encontrado"))


@app.errorhandler(500)
def erro_interno(error):
    return redirect(url_for("erro.erro_interno"))


if __name__ == "__main__":
    app.run()
