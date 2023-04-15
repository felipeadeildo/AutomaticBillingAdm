from flask import Blueprint, render_template, url_for, g, abort, flash, request
from .db import get_db
from .auth import login_required, can_access
from MySQLdb._exceptions import IntegrityError

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db()
    features = conn.execute('SELECT * FROM features').fetchall()
    context = {
        'categorys': list(set([c['category'] for c in features])),
        'features': features
    }
    return render_template('home/index.html', **context)


@bp.route('/addclient', methods=("POST", "GET"))
@login_required
def addclient():
    if not can_access():
        flash("Olá, infelizmente você não nível de permissão suficiente para acessar essa página, como chegastes até aqui?")
        abort(403)
        
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (name, username, email, password, role) VALUES (%s, %s, %s, %s, %s)',
                (name, username, email, password, role)
            )
        except IntegrityError:
            error = f'O nome de usuário "{username}" ou o e-mail "{email}" já existe no banco de dados'
        else:
            conn.commit()
        if error is not None:
            flash(error, category='danger')
        else:
            flash(f"Usuário {username} adicionado com sucesso", category="success")
    context = {
        "previous_page": "home.index"
    }
    return render_template('home/addclient.html', **context)


@bp.route('/reports')
@login_required
def reports():
    return "Em produção"

@bp.route('/editclient')
@login_required
def editclient():
    return "Em produção"

@bp.route('/settings')
@login_required
def settings():
    return "Em produção"
