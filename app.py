# coding: utf-8
from datetime import timedelta

from flask import Flask, redirect, url_for
from mod_home.home import bp_home
from mod_pedido.pedido import bp_pedido
from mod_erro.erro import bp_erro
from mod_produto.produto import bp_produto
from mod_cliente.cliente import bp_cliente
from mod_login.login import bp_login


app = Flask(__name__)

app.secret_key = b'_8#y2P"g8l1x\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(bp_home)
app.register_blueprint(bp_pedido)
app.register_blueprint(bp_erro)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_login)


@app.errorhandler(404)
def nao_encontrado(error):
    return redirect(url_for("erro.nao_encontrado"))


@app.errorhandler(500)
def erro_interno(error):
    return redirect(url_for("erro.erro_interno"))


if __name__ == "__main__":
    app.run()
