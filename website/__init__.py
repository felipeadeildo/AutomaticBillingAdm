from flask import Flask
from dotenv import dotenv_values

config = dotenv_values(".env")

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(**config)
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    
    return app
