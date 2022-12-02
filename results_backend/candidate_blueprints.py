from flask import Blueprint, request
import requests

from utils import HEADERS, load_file_config

candidate_blueprints = Blueprint("candidate_blueprints", __name__)
data_config = load_file_config()
url_base = data_config.get('url-backend-results') + "/candidate"


@candidate_blueprints.route("/candidates", methods=['Get'])
def get_all_candidates() -> dict:
    url = f'{url_base}/all'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@candidate_blueprints.route("/candidate/<string:id_>", methods=['GET'])
def get_candidate_by_id(id_: str) -> dict:
    url = f'{url_base}/{id_}'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@candidate_blueprints.route("/candidate/insert", methods=['POST'])
def insert_candidate() -> dict:
    candidate = request.get_json()
    party_id = candidate.get('political_party').get('_id')
    del candidate['political_party']
    url = f'{url_base}/insert'
    response = requests.post(url, headers=HEADERS, json=candidate)
    candidate_id = response.json().get('_id')
    url_relation = f'{url_base}/{candidate_id}/political_party/{party_id}'
    response = requests.post(url, headers=HEADERS, json=candidate)
    return response.json()


@candidate_blueprints.route("/candidate/update/<string:id_>", methods=['PUT'])
def update_candidate(id_: str) -> dict:
    candidate = request.get_json()
    url = f'{url_base}/update/{id_}'
    response = requests.patch(url, headers=HEADERS, json=candidate)
    return response.json()


@candidate_blueprints.route("/candidate/delete/<string:id_>", methods=['DELETE'])
def delete_candidate(id_: str) -> dict:
    url = f'{url_base}/delete/{id_}'
    response = requests.delete(url, headers=HEADERS)
    return response.json()
