from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from app.db import initialize_db
from flask_cors import CORS

# Declare the flask app and wrap it in Api
app = Flask(__name__)
CORS(app)

api = Api(app)

from app import config
from app import routes

# Define the environment status
if config.env == 'DEVELOPMENT':
    conf = config.DevelopmentConfig
else:
    conf = config.ProductionConfig

app.config.from_object(conf)

initialize_db(app)


# Define the route where swagger will find the data to generate /api/docs
@app.route("/swagger")
def swaggerController():
    # Spec file for marshmallow
    swag = swagger(app)
    swag['info']['version'] = config.APP_VERSION
    swag['info']['title'] = config.API_NAME
    return jsonify(swag)

# Define the blueprint of the API
swaggerui_blueprint = get_swaggerui_blueprint(
    conf.SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    conf.DATA_SWAGGER,
    config = {  # Swagger UI config overrides
        'app_name': "Flask API"
    },
)

print("Routes :")
print('/account : POST 🍏') 
print('/login : POST 🍏') 
print('/lists : GET 🍏 | PUT 🍏')
print('/lists/<str:list_id> : GET 🍏 | DELETE 🍏 | PATCH 🍏')
print('/lists/todos/<str:id_list> : GET 🍏 | PUT 🍏')
print('/lists/todos/<str:list_id>/<str:todo_id> : GET 🍏 | DELETE 🍏 | PATCH 🍏')

app.register_blueprint(swaggerui_blueprint, url_prefix=conf.SWAGGER_URL)
