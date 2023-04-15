from flask import Flask, redirect, url_for
from dotenv import dotenv_values

config = dotenv_values(".env")

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(**config)
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    
    from . import home
    app.register_blueprint(home.bp)
    
    from . import client
    app.register_blueprint(client.bp)
    
    
    @app.route("/")
    def index(): return redirect(url_for("home.index"))
    
    @app.errorhandler(403)
    def forbbiden(e): return "403 Forbbiden (Você não tem permissaõ de acessar essa página :D)"
    
    return app