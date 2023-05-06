from flask import Blueprint, request, g, render_template, flash
from .db import get_db
from .auth import login_required
from datetime import datetime
from .settings import TIPOS_IMOVEIS

bp = Blueprint("enterprise", __name__, url_prefix="/client")

@bp.route("/settings")
@login_required()
def settings():
    return "Em produção"


@bp.route("/adicionar-inquilino", methods=("POST", "GET"))
@login_required()
def add_resident():
    enterprise_id = g.user["enterprise_id"]
    conn = get_db()
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"] # TODO Validar CPF (pelo menos um len(cpf) == 11)
        cpf = "".join(x for x in cpf if x.isdigit())
        telefone = request.form["telefone"] # TODO: Sanitizar telefone
        email = request.form["email"]
        prazo_tolerancia = request.form["prazo_tolerancia"]
        prazo_medidas_legais = request.form["prazo_medidas_legais"]
        data_inicio = datetime.strptime(request.form["data_inicio"], "%B %d, %Y") # May 26, 2023
        data_termino = datetime.strptime(request.form["data_termino"], "%B %d, %Y")
        imovel_id = request.form["imovel_id"]
        # TODO: Verificar se imovel_id realmente existe
        
        enterprise_id = request.form["enterprise_id"]
        
        conn.execute(
            "INSERT INTO morador (nome, cpf, telefone, email, imovel_id, enterprise_id, prazo_tolerancia, prazo_medidas_legais, data_inicio, data_termino) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (nome, cpf, telefone, email, imovel_id, enterprise_id, prazo_tolerancia, prazo_medidas_legais, data_inicio, data_termino)
        )
        conn.commit()
        flash(f"Morador {nome} ({email}) foi adicionado com sucesso ao banco de dados relacionado ao imóvel de id {imovel_id}", category="success")
    
    imoveis = conn.execute("SELECT * FROM imovel WHERE id NOT IN (SELECT imovel_id FROM morador) AND enterprise_id = %s", (enterprise_id, )).fetchall()
    enterprises = conn.execute("SELECT * FROM empresa").fetchall()
    context = {
        "imoveis": imoveis,
        "enterprise_id": enterprise_id, # can be None
        "enterprises":  enterprises,
        "previous_page": "home.index"
    }
    return render_template("enterprise/add_resident.html", **context)
        

@bp.route("/adicionar-imovel", methods=("POST", "GET"))
@login_required()
def add_property():
    conn = get_db()
    enterprise_id = g.user["enterprise_id"]
    if request.method == 'POST':
        enterprise_id = request.form["enterprise_id"]
        valor_aluguel = request.form["valor_aluguel"]
        valor_venda = request.form["valor_venda"]
        taxa_adm_mensal = request.form["taxa_adm_mensal"]
        taxa_locacao = request.form["taxa_locacao"]
        cep = request.form["cep"]
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        tipo = request.form['tipo']
        conn.execute(
            "INSERT INTO imovel (enterprise_id, valor_aluguel, valor_venda, taxa_adm_mensal, taxa_locacao, cep, endereco, numero, complemento, bairro, cidade, estado, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (enterprise_id, valor_aluguel, valor_venda, taxa_adm_mensal, taxa_locacao, cep, endereco, numero, complemento, bairro, cidade, estado, tipo)
        )
        conn.commit()
        imovel_name = f"{endereco} {numero} {complemento}"
        flash(f"Imóvel {imovel_name} foi adicionado com sucesso ao banco de dados", category="success")
    
    enterprises = conn.execute("SELECT * FROM empresa").fetchall()
    context = {
        "enterprise_id": enterprise_id, # can be None
        "enterprises":  enterprises,
        "tipos_imovel": TIPOS_IMOVEIS,
        "previous_page": "home.index"
    }
    return render_template("enterprise/add_house.html", **context)


@bp.route("/inquilinos")
@login_required()
def listinquilinos():
    return "Em produção"