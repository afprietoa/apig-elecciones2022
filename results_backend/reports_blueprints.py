from flask import Blueprint
import requests

from utils import load_file_config, HEADERS

reports_blueprints = Blueprint("reports_blueprint", __name__)
data_config = load_file_config()
url_base = data_config.get('url-backend-results') + "/reports"


@reports_blueprints.route("/reports/table_votes/all", methods=['GET'])
def report_table_votes() -> dict:
    url = f'{url_base}/table_votes/all'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@reports_blueprints.route("/reports/candidate_votes/all", methods=['GET'])
def report_candidate_votes() -> dict:
    url = f'{url_base}/candidate_votes/all'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@reports_blueprints.route("/reports/party_votes/all", methods=['GET'])
def report_party_votes() -> dict:
    url = f'{url_base}/party_votes/all'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@reports_blueprints.route("/reports/general_distribution", methods=['GET'])
def report_general_distribution() -> dict:
    url = f'{url_base}/general_distribution'
    response = requests.get(url, headers=HEADERS)
    return response.json()