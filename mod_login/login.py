# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import wraps
import time

bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')


def logado(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login.entrar'))
        return f(*args, **kwargs)
    return decorated_function


@bp_login.route('/')
def entrar():
    erro = request.args.get('erro')
    mensagem = 'Credenciais inválidas, tente novamente!'
    if erro == '2':
        mensagem = 'Sua sessão expirou, faça login novamente!'

    return render_template('formLogin.html', erro=erro, mensagem=mensagem), 200


@bp_login.route('/login', methods=['POST'])
def login():
    usuario = request.form.get('login')
    senha = request.form.get('senha')
    realusuario = 'abc'
    realsenha = 'Bolinhas'
    if usuario == realusuario and senha == realsenha:
        session.permanent = True
        session['login'] = usuario
        session['time'] = time.time()
        return redirect(url_for('home.home'))
    return redirect(url_for('login.entrar', erro=1))


@bp_login.route('/logout')
def sair():
    session.pop('login', None)
    return redirect(url_for('login.entrar'))
