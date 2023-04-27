from flask import Blueprint

from .auth import login_required


bp = Blueprint("enterprise", __name__, url_prefix="/client")

@bp.route("/settings")
@login_required()
def settings():
    return "Em produção"


@bp.route("/addinquilino")
@login_required()
def add_resident():
    return "Em produção"


@bp.route("/addhouse")
@login_required()
def add_property():
    return "Em produção"

@bp.route("/inquilinos")
@login_required()
def listinquilinos():
    return "Em produção"