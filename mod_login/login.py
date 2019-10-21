# coding: utf-8
from flask import Blueprint, render_template, redirect, url_for, request, session
from functools import wraps
import time

bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')

SESSION_LIMIT = 30


def logado(f):
    """Verifica se usuario esta logado, impede que acesse o site caso tenha atingido o limite de tempo na sessao"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login.entrar'))
        if 'time' in session:
            now = time.time()
            diff_seconds = now - session['time']
            diff_minutes = diff_seconds / 60
            if diff_minutes >= SESSION_LIMIT:
                return redirect(url_for('login.entrar', erro=2))
        return f(*args, **kwargs)
    return decorated_function


@bp_login.route('/')
def entrar():
    erro = request.args.get('erro')
    mensagem = None
    if erro == '1':
        mensagem = 'Credenciais inválidas, tente novamente!'
    elif erro == '2':
        mensagem = 'Sua sessão expirou, faça login novamente!'

    return render_template('formLogin.html', mensagem=mensagem), 200


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
