from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from database.models import db
from cli.cli import custom_cli
from services.open_food_fact import setup_open_food_fact
from resources.users import UsersApi, UserApi
from resources.auth import SignupApi, LoginApi, SessionAPI
from resources.products import ProductsAPI, ProductAPI, ProductBuyAPI
from resources.rankings import UserRankingAPI, ProductRankingAPI

app = Flask(__name__, instance_relative_config=True)
app.config['JSON_SORT_KEYS'] = False

# Loads configuration from config.py
app.config.from_object('config')
## From here you can access config variables like this:
## value_from_config = app.config['CONFIG_VARIABLE_NAME']

## Initialisation des modules
db.init_app(app)
custom_cli(app)
migrate = Migrate(app, db)
setup_open_food_fact(app)
api = Api(app)
Bcrypt(app)
JWTManager(app)

## Declaration of API routes

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')
api.add_resource(SessionAPI, '/auth/me')

## User routes

api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/users/<userId>')
# api.add_resource(UsersRankingsAPI, '/rankings/users')

## Product routes

api.add_resource(ProductsAPI, '/products')
api.add_resource(ProductAPI, '/products/<bar_code>')
api.add_resource(ProductBuyAPI, '/products/buy')

## Ranking routes

api.add_resource(UserRankingAPI, '/rankings/users')
api.add_resource(ProductRankingAPI, '/rankings/products')


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World from Food Buy API"})
