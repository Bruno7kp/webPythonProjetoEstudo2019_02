# coding: utf-8
from flask import Blueprint, render_template, session
from mod_login.login import logado

bp_home = Blueprint('home', __name__, url_prefix='/', template_folder='templates')


@bp_home.route("/home")
@logado
def home():
    return render_template("home.html"), 200


