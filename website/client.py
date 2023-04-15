from flask import Blueprint

from .auth import login_required


bp = Blueprint("client", __name__, url_prefix="/client")

@bp.route("/settings")
@login_required()
def settings():
    return "Em produção"