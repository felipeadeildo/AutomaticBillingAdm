from flask import Blueprint, render_template, url_for, g, abort, flash, request
from .db import get_db
from .auth import login_required
from MySQLdb._exceptions import IntegrityError
from werkzeug.security import generate_password_hash
from .settings import CLIENTE_PERM_LEVEL

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required()
def index():
    conn = get_db()
    features = conn.execute('SELECT * FROM features').fetchall()
    context = {
        'categorys': list(set([(c['category'], c['min_perm_level']) for c in features])),
        'features': features
    }
    return render_template('home/index.html', **context)


@bp.route('/addclient', methods=("POST", "GET"))
@login_required(level_access='empresa')
def addclient(): 
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        role = 'cliente'
        # TODO: Adicionar validação de campos
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (name, username, email, password, role, permission_level) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, username, email, password, role, CLIENTE_PERM_LEVEL)
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

@bp.route("/clients")
@login_required(level_access='empresa')
def clients():
    conn = get_db()
    clients = conn.execute('SELECT * FROM users WHERE role = "cliente"').fetchall()
    context = {
        'clients': clients
    }
    return render_template('home/clients.html', **context)

@bp.route('/reports')
@login_required()
def reports():
    return "Em produção"

@bp.route('/editclient')
@login_required(level_access='empresa')
def editclient():
    return "Em produção"

@bp.route('/settings')
@login_required(level_access='empresa')
def settings():
    return "Em produção"