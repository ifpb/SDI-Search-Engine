from flask import Flask, request, make_response, jsonify

from request_status.multiple_choices import HttpMultipleChoices
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound
from service import query_service
import json
from flask_cors import CORS, cross_origin

build_json = (lambda v: json.dumps(v, default=lambda o: o.__dict__))

app = Flask(__name__)


@app.route('/find-place/level-service/', methods=['POST'])
@cross_origin()
def find_place():
    try:
        data = request.get_json()
        place_name = data['place-name']
        app.logger.debug('request find-place: ' + place_name)
        list_services = query_service.find_place_in_level_service(place_name)
        return jsonify(list_services)
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except HttpMultipleChoices as e:
        return make_response(jsonify(e.message), e.code)
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)


@app.route('/find-place/level-feature-type/', methods=['POST'])
@cross_origin()
def find_feature_types():
    try:
        data = request.get_json()
        place_name = data['place-name']
        app.logger.debug('request find-place: ' + place_name)
        return jsonify(query_service.find_place_in_level_feature_type(place_name))
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except HttpMultipleChoices as e:
        return make_response(jsonify(e.message), e.code)
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)


@app.route('/test')
@cross_origin()
def find_place_service():
    query_service.test_find_services()


if __name__ == '__main__':
    app.run(debug=True)
