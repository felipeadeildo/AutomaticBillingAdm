from flask import current_app, g
import MySQLdb
import click
from werkzeug.security import generate_password_hash

class DBResponse:
    def __init__(self, cursor, conn) -> None:
        self.conn = conn
        self.cursor = cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, quantidade: int):
        return self.cursor.fetchmany(quantidade)

class Connection:
    def __init__(self) -> None:
        configs = current_app.config.copy()
        self.conn = MySQLdb.connect(
            host=configs["DB_HOST"],
            port=int(configs["DB_PORT"]),
            user=configs["DB_USER"],
            password=configs["DB_PASSWORD"],
            database=configs["DB_NAME"],
        )
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
    
    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()

    def execute(self, query: str, params: tuple = None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return DBResponse(self.cursor, self.conn)


def get_db():
    if not "db" in g:
        g.db = Connection()
    return g.db

def close_db(e=None):
    conn: Connection = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    config = current_app.config
    db = MySQLdb.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        port=int(config["DB_PORT"]),
        password=config["DB_PASSWORD"]
    )
    
    cursor = db.cursor()
    with open("schema.sql", "r", encoding="utf-8") as f:
        cursor.execute(f.read().replace('__DBNAME__', config['DB_NAME']))
    
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)", 
        ('Adicionar Empresa', 'Adiciona uma nova empresa (que possui imóveis e seus próprios clientes)', 'ADM Master', 80, 'home.add_enterprise')
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Lista de Empresas', "Lista de todas as empresas cadastrados com mais algumas informações (quantidade de clientes, imóveis e etc.) e opções.", 'ADM Master', 80, "home.list_enterprises")
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Editar Empresas', 'Pesquisar e editar informações uma empresa em específico.', 'ADM Master', 80, 'home.edit_enterprise')
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Relatórios', 'Mostra informações de relatórios, estatísticas gerais', 'ADM Master', 80, 'home.reports')
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Configurações', "Configurações do sistema; Configurações referentes à frequência de cobranças, taxa padrão de juros, etc.", 'ADM Master', 80, "home.settings")
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Configurações', "Configuraçães do sistema; Configurações referentes à taxa padrão de juros, etc.", 'Empresa', 50, "enterprise.settings")
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Adicionar Cliente', "Permite adicionar cliente (morador) relacionado à um imóvel determinando um valor de pagamento, email, telefone e etc.", 'Empresa', 50, "enterprise.add_resident")
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Adicionar Imóvel', "Permite adicionar um imóvel para que seja possível adicionar cliente (morador) na mesma; Informações incluem endereço, valor mensal do aluguel, tipo da casa e etc.", 'Empresa', 50, "enterprise.add_property")
    )
    
    cursor.execute(
        "INSERT INTO feature (name, description, category, min_perm_level, import_url) VALUES (%s, %s, %s, %s, %s)",
        ('Lista de Clientes', "Lista todos os clientes dentro do banco de dados de uma determinada empresa.", 'Empresa', 50, "enterprise.list_residents")
    )
    
    db.commit()
    


@click.command("init-db")
def init_db_command():
    """Limpa o banco de dados existente e cria novas tabelas"""
    init_db()
    click.echo("O banco de dados foi inicializado!")


def create_superuser(name, username, email, password):
    """Cria um superusuário com os dados fornecidos
    Args:
        name (str): nome do superuser
        username (str): username para login do superuser
        email (str): email do superuser
        password (str): senha do superuser
    """
    db = get_db()
    db.execute(
        "INSERT INTO user (name, username, email, password, permission_level, role) VALUES (%s, %s, %s, %s, 100, %s)",
        (name, username, email, generate_password_hash(password), 'Administrador')
    )
    db.commit()
    
@click.command('createsuperuser')
@click.option("--name", prompt=True, help="O nome do superusuário")
@click.option("--username", prompt=True, help="O nome de usuário do superusuário")
@click.option("--email", prompt=True, help="O email do superusuário")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="A senha do superusuário")
def create_superuser_command(name, username, email, password):
    """Cria um superusuário para a aplicação"""
    create_superuser(name, username, email, password)
    click.echo("O superusuário foi criado com sucesso!")


def init_app(app):
    """Faz a inicialização do APP adicionando algumas funcionalidades do DB de início
    Args:
        app (flask.Flask): aplicação flask instanciada.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
    app.cli.add_command(create_superuser_command)