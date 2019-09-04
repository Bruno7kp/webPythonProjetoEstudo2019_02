# coding: utf-8
from flask import Blueprint, render_template

bp_erro = Blueprint('erro', __name__, url_prefix='/', template_folder='templates')


@bp_erro.route('/404')
def nao_encontrado():
    return render_template("form404.html"), 404


@bp_erro.route('/500')
def erro_interno():
    return render_template("form500.html"), 500
