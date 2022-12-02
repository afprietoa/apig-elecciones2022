from flask import Flask, request
from flask_cors import CORS
from waitress import serve
from flask import jsonify
from flask_jwt_extended import (JWTManager, create_access_token, verify_jwt_in_request,
                                get_jwt_identity)
import requests as rq
from datetime import timedelta
import utils
from results_backend.candidate_blueprints import candidate_blueprints
from security_backend.permission_blueprints import permission_blueprints
from results_backend.political_party_blueprints import political_party_blueprints
from security_backend.rol_blueprints import rol_blueprints
from results_backend.table_blueprints import table_blueprints
from security_backend.user_blueprints import user_blueprints
from results_backend.vote_blueprints import vote_blueprints
from results_backend.reports_blueprints import reports_blueprints

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "superKey"
cors = CORS(app)
jwt = JWTManager(app)
app.register_blueprint(candidate_blueprints)
app.register_blueprint(permission_blueprints)
app.register_blueprint(political_party_blueprints)
app.register_blueprint(rol_blueprints)
app.register_blueprint(table_blueprints)
app.register_blueprint(user_blueprints)
app.register_blueprint(vote_blueprints)
app.register_blueprint(reports_blueprints)


@app.before_request
def before_request_callback() -> tuple:
    endpoint = utils.clear_url(request.path)
    exclude_routes = ['/', '/login']
    if exclude_routes.__contains__(request.path):
        pass
    elif verify_jwt_in_request():
        user = get_jwt_identity()
        if user.get('rol'):
            has_grant = utils.validate_grant(endpoint, request.method, user['rol'].get('idRol'))
            if not has_grant:
                return {"message": "Access denied by grant."}, 401
        else:
            return {"message": "Access denied by left rol."}, 401


@app.route("/", methods=['GET'])
def home() -> dict:
    response = {"message": "Welcome to the Results API Gateway ..."}
    return jsonify(response)


@app.route("/login", methods=['POST'])
def login() -> tuple:
    user = request.get_json()
    url = data_config.get('url-backend-security') + '/user/login'
    response = rq.post(url, headers=utils.HEADERS, json=user)
    if response.status_code == 200:
        user_logged = response.json()
        del user_logged['rol']['permissions']
        expires = timedelta(days=1)
        access_token = create_access_token(identity=user_logged, expires_delta=expires)
        return {"token": access_token, "user_id": user_logged.get('id')}, 200
    else:
        return {"message": "Access denied."}, 401


if __name__ == '__main__':
    data_config = utils.load_file_config()
    print(f'API Gateway Server running...: http://{data_config.get("url-api-gateway")}'+
          f':{data_config.get("port")}')
    serve(app, host=data_config.get('url-api-gateway'), port=data_config.get('port'))
