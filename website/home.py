from flask import Blueprint, render_template, flash, request, abort
from .db import get_db
from .auth import login_required
from werkzeug.security import generate_password_hash
from .settings import EMPRESA_PERM_LEVEL, PAGINATION_EMPRESAS

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required()
def index():
    conn = get_db()
    features = conn.execute('SELECT * FROM feature').fetchall()
    context = {
        'categorys': list(set([(c['category'], c['min_perm_level']) for c in features])),
        'features': features
    }
    return render_template('home/index.html', **context)



@bp.route('/adicionar-empresa', methods=("POST", "GET"))
@login_required(level_access="adm")
def add_enterprise(): 
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        name_user = request.form.get('name_user')
        email_user = request.form.get("email_user")
        # TODO: Adicionar validação de campos
        conn = get_db()
        user_already_exists = conn.execute("SELECT * FROM user WHERE username = %s", (username, )).fetchone()
        enterprise_already_exists = conn.execute("SELECT * FROM empresa WHERE email = %s", (email,)).fetchone()
        f"Já existe um usuário com username {username}, use outro."
        if (user_already_exists is None and enterprise_already_exists is None):
            conn.execute(
                'INSERT INTO empresa (name, email) VALUES (%s, %s)',
                (name, email)
            )
            conn.commit()
            enterprise_id = conn.execute("SELECT id FROM empresa WHERE email = %s", (email, )).fetchone()["id"]
            
            conn.execute("INSERT INTO user (username, password, email, name, role, permission_level, enterprise_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (username, generate_password_hash(password), email_user, name_user, 'Empresa', EMPRESA_PERM_LEVEL, enterprise_id))
            conn.commit()
            flash(f'Empresa "{name}" adicionado com sucesso', category="success")
        else:
            if user_already_exists is not None:
                flash(f"O username {username} já existe no banco de dados, troque por outro", category='danger')
                
            if enterprise_already_exists is not None:
                flash(f"O email {email} já existe no banco de dados, troque por outro", category='danger')
    context = {
        "previous_page": "home.index"
    }
    return render_template('home/add_enterprise.html', **context)

@bp.route("/empresas")
@login_required(level_access="adm")
def list_enterprises():
    n_page = int(request.args.get("page", 0))
    conn = get_db()
    enterprises = conn.execute(
        'SELECT * FROM empresa LIMIT {}, {}'.format(n_page*PAGINATION_EMPRESAS, PAGINATION_EMPRESAS)
    ).fetchall() # TODO: Tratar quando não houver empresas (empresas == ())
    
    total_enterprises = conn.execute(
        "SELECT COUNT(*) FROM empresa"
    ).fetchone()['COUNT(*)']
    total_pages = total_enterprises // PAGINATION_EMPRESAS
    pagination_info = {
        "current_page": n_page,
        "has_prev": bool(n_page),
        "has_next": len(enterprises) == PAGINATION_EMPRESAS and (n_page+1)*PAGINATION_EMPRESAS != total_enterprises,
        "prev_num": n_page - 1,
        "next_num": n_page + 1,
        "total_pages": total_pages if total_pages > 0 else 1
    }
    context = {
        'empresas': enterprises,
        "pagination_info": pagination_info
    }
    return render_template('home/list_enterprises.html', **context)

@bp.route('/reports')
@login_required()
def reports():
    return "Em produção"

@bp.route('/editar-empresa-id/<int:enterprise_id>')
@login_required(level_access='adm')
def edit_enterprise_id(enterprise_id:int):
    conn = get_db()
    enterprise_infos = conn.execute("SELECT * FROM empresa WHERE id = %s", (enterprise_id, )).fetchone()
    if enterprise_infos is None:
        abort(404)
    
    if request.method == "POST":
        # TODO: Editar no banco de dados
        pass
    
    default_user = conn.execute("SELECT * FROM user WHERE enterprise_id = %s ORDER BY id DESC", (enterprise_id, )).fetchone()
    enterprise_infos = conn.execute("SELECT * FROM empresa WHERE id = %s", (enterprise_id, )).fetchone()
    
    context = {
        "enterprise": enterprise_infos,
        "enterprise_user": default_user,
        "previous_page": "home.index"
    }
    
    return render_template("home/edit_enterprise_id.html", **context)
    
    

@bp.route("/editar-empresa")
@login_required(level_access='adm')
def edit_enterprise():
    return "Em produção"

@bp.route('/settings')
@login_required(level_access='adm')
def settings():
    return "Em produção"

@bp.route('/empresa/<int:enterprise_id>')
@login_required(level_access='adm')
def enterprise_infos(enterprise_id:int):
    return "Em produção"