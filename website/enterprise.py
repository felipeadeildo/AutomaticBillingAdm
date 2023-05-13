from flask import Blueprint, request, g, render_template, flash, abort
from .db import get_db
from .auth import login_required
from datetime import datetime
from .settings import TIPOS_IMOVEIS, EMPRESA_PERM_LEVEL, PAGINATION_CLIENTS, ADM_MIN_PERM_LEVEL

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
        data_inicio = datetime.strptime(request.form["data_inicio"], "%b %d, %Y") # May 26, 2023
        data_termino = datetime.strptime(request.form["data_termino"], "%b %d, %Y")
        imovel_id = request.form["imovel_id"]
        dia_pagamento = request.form["data_pagamento"]
        # TODO: Adicionar handler para tratar o dia de pagamento e salvar no db
        data_pagamento = datetime.now()
        # TODO: Verificar se imovel_id realmente existe
        
        enterprise_id = request.form["enterprise_id"]
        
        conn.execute(
            "INSERT INTO morador (nome, cpf, telefone, email, imovel_id, enterprise_id, prazo_tolerancia, prazo_medidas_legais, data_inicio, data_termino, data_pagamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (nome, cpf, telefone, email, imovel_id, enterprise_id, prazo_tolerancia, prazo_medidas_legais, data_inicio, data_termino, data_pagamento)
        )
        conn.commit()
        flash(f"Morador {nome} ({email}) foi adicionado com sucesso ao banco de dados relacionado ao imóvel de id {imovel_id}", category="success")
    
    if g.user["permission_level"] >= EMPRESA_PERM_LEVEL:
        imoveis = conn.execute(
            "SELECT * FROM imovel WHERE id NOT IN (SELECT imovel_id FROM morador)"
        ).fetchall()
        empresas = conn.execute(
            "SELECT id, name, email FROM empresa WHERE id IN (SELECT enterprise_id FROM imovel WHERE id NOT IN (SELECT imovel_id FROM morador))"
        ).fetchall()

        # Combine the results into a single list of dictionaries
        result = []
        for imovel in imoveis:
            empresa = next((e for e in empresas if e["id"] == imovel["enterprise_id"]), None)
            if empresa:
                result.append({**imovel, **empresa})
        imoveis = result.copy()
    else:
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
def list_residents():
    """Tem que fazer uma visualização paginada de clientes numa determinada empresa"""
    enterprise_id = g.user["enterprise_id"] if request.args.get("enterprise_id") is None else request.args["enterprise_id"]
    # se na requisição não possui parâmetro para enterprise_id, então o usuário está relacionado à uma empresa, se não, pega da querystirng
    # TODO: Erro de segurança: if g.user["enterprise_id"] is not None and request.args.get("enterprise_id") is not None
    # pode ser uma empresa tentando acessar o id de OUTRA empresa... (exemplo)

    page = request.args.get('page', 1, type=int)
    has_prev = None
    has_next = None
    conn = get_db()

    clients = []
    if enterprise_id is not None:
        total = conn.execute(
            "SELECT COUNT(*) FROM morador WHERE enterprise_id = %s", 
            (enterprise_id, )
        ).fetchone()["COUNT(*)"]
        clients = conn.execute(
            "SELECT * FROM morador WHERE enterprise_id = %s LIMIT %s OFFSET %s", 
            (enterprise_id, PAGINATION_CLIENTS, (page - 1) * PAGINATION_CLIENTS)
        ).fetchall()
        has_prev = page > 1
        has_next = page * PAGINATION_CLIENTS < total

    enterprises = conn.execute("SELECT * FROM empresa").fetchall()
    context = {
        "clients": clients,
        "enterprise_id": enterprise_id,
        "enterprises": enterprises,
        "page": page,
        "has_prev": has_prev,
        "has_next": has_next,
        "prev_num": page - 1,
        "next_num": page + 1,
        "pages": list(range(0, len(clients)//PAGINATION_CLIENTS))
    }

    return render_template("enterprise/list_residents.html", **context)


@bp.route("/propiedadeaquió/<int:imovel_id>")
@login_required()
def property_infos(imovel_id:int):
    return "Em produção"


@bp.route("/clienteaquió/<int:client_id>", methods=("POST", "GET"))
@login_required()
def client_infos(client_id:int):
    conn = get_db()
    morador = conn.execute("SELECT * FROM morador WHERE id = %s", (client_id,)).fetchone()

    # verifica se o morador_id existe
    if morador is None:
        flash(f"Morador de ID {client_id} não foi encontrado no DB", category="danger")
        abort(404)
    # verifica se a empresa que está tentando acessar realmente tem perm pra isso
    if morador["enterprise_id"] != g.user["enterprise_id"] and g.user["permission_level"] < ADM_MIN_PERM_LEVEL:
        abort(403)
    

    if request.method == "POST":
        # se chegou até aqui é pq está tudo okay :D
        status = request.form["status"]
        conn.execute("UPDATE morador SET status = %s WHERE id = %s", (status, client_id))
        conn.commit()
        flash(f"Status do morador {morador['nome']} foi atualizado com sucesso!", category="success")
        morador["status"] = int(status)

    enterprise = conn.execute("SELECT * FROM empresa WHERE id = %s", (morador["enterprise_id"], )).fetchone()

    imovel = conn.execute("SELECT * FROM imovel WHERE id = %s", (morador["imovel_id"], )).fetchone()

    pagamentos = conn.execute("SELECT * FROM pagamento WHERE morador_id = %s ORDER BY data_pagamento DESC", (morador["id"], )).fetchall()

    mes_atual = datetime.now().strftime("%m")
    ultimo_mes_pago = pagamentos[0] if len(pagamentos) > 0 else None
    data_ultimo_pagamento = pagamentos[0] if len(pagamentos) > 0 else None
    context = {
        "enterprise": enterprise,
        "morador": morador,
        "imovel": imovel,
        "ultimo_mes_pago": ultimo_mes_pago,
        "mes_atual": mes_atual,
        "data_ultimo_pagamento": data_ultimo_pagamento
    }
    return render_template("enterprise/client_infos.html", **context)


@bp.route("/relatórios")
@login_required()
def reports():
    return "Em produção"