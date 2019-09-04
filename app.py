# coding: utf-8
from flask import Flask, redirect, url_for
from mod_home.home import bp_home
from mod_pedido.pedido import bp_pedido
from mod_erro.erro import bp_erro

app = Flask(__name__)

app.register_blueprint(bp_home)
app.register_blueprint(bp_pedido)
app.register_blueprint(bp_erro)


@app.errorhandler(404)
def nao_encontrado(error):
    return redirect(url_for("erro.nao_encontrado"), code=302)


@app.errorhandler(500)
def erro_interno(error):
    return redirect(url_for("erro.erro_interno"), code=302)


if __name__ == "__main__":
    app.run()
