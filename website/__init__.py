from flask import Flask, redirect, url_for, render_template, flash
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
    def forbbiden(e): return render_template("403.html"), 403
    
    @app.errorhandler(404)
    def notfound(e):
        flash("Página não encontrada!", category="danger")
        return render_template("404.html"), 404
    
    return app