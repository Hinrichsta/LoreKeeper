from flask import Flask
from Database.Database import Lore_Session

def create_app():
    app = Flask(__name__)

    from .views import money

    app.register_blueprint(money.money, url_prefix='/')
    
    return app
