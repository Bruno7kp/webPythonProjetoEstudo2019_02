# coding: utf-8
from flask import Flask, render_template, Blueprint
from mod_home.home import bp_home
from mod_pedido.pedido import bp_pedido

app = Flask(__name__)

app.register_blueprint(bp_home)
app.register_blueprint(bp_pedido)


@app.errorhandler(404)
def nao_encontrado(error):
    return render_template("form404.html"), 404


@app.errorhandler(500)
def erro_interno(error):
    return render_template("form500.html"), 500


if __name__ == "__main__":
    app.run()
