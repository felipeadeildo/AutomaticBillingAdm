from flask import Blueprint, render_template, url_for
from .db import get_db
from .auth import login_required

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


@bp.route('/addclient')
@login_required
def addclient():
    return "Em produção"

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
