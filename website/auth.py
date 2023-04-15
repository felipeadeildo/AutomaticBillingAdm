from flask import Blueprint, g, request, render_template, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from .db import get_db
import functools
from .settings import EMPRESA_MIN_PERM_LEVEL, CLIENTE_PERM_LEVEL

bp = Blueprint("auth", __name__) # este blueprint tem que apontar para index

@bp.route("/login", methods=("POST", "GET"))
def login():
    if g.user is not None:
        flash(f"Você já está logado como {g.user['name']}, por que tentas logar novamente?")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = %s",
            (username, )
        ).fetchone()
        if user is None:
            error = "Usuário e/ou Senha estão incorretos"
        elif not check_password_hash(user['password'], password):
            error = "Usuário e/ou Senha estão incorretos"
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = %s',
            (user_id, )
        ).fetchone()

def login_required(view):
    """Decorador para definir que a view deve ser protegida por login
    Args:
        view (flask.views): View em questão
    Returns:
        view: view normal, caso esteja logado
        redirect: caso não tenha permissão de acessar aquela rota
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Você precisa está logado para acessar a página solicitada!')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Você foi deslogado com sucesso!")
    return redirect(url_for('auth.login'))

def can_access(access_type:str='empresa') -> bool:
    """Define se o usuário atual tem permissão a um certo tipo de acesso

    Args:
        access_type (str, optional): Tipo de acesso, pode ser 'empresa' ou 'cliente'. Defaults to 'empresa'.

    Returns:
        bool: Confirmação
    """
    if access_type == 'empresa':
        return g.user["permission_level"] >= EMPRESA_MIN_PERM_LEVEL
    elif access_type == 'cliente':
        return g.user['permissio_level'] >= CLIENTE_PERM_LEVEL
    else:
        raise "Tipo de acesso não suportado, tem certeza que digitou corretamente?"