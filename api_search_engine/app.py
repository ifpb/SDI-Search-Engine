from flask import Flask, request, make_response, jsonify
import log
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound
from service import query_service, MultipleChoices as mc
import json
from flask_cors import CORS, cross_origin

build_json = (lambda v: json.dumps(v, default=lambda o: o.__dict__))

app = Flask(__name__)

""" Obtem o log padão da aplicação """
app_log = log.get_logger()


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
    except mc.MultipleChoices as e:
        return jsonify(query_service.retrieve_all_places(e.data)), e.code
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
    except mc.MultipleChoices as e:
        return jsonify(query_service.retrieve_all_places(e.data)), 300
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)


@app.route('/find-place/choice', methods=['POST'])
@cross_origin()
def by_choice_find_place():
    try:
        data = request.get_json()
        place = data["choice"]
        app_log.info(str(place["id"]) + place["name"])
        level = request.args.get("level")
        if level == "SERVICE":
            app_log.info("choice in level of the service")
            result = query_service.find_place_in_level_service(place["id"], True)
        else:
            app_log.info("choice in level of the feature type")
            result = query_service.find_place_in_level_feature_type(place["id"], True)
        return jsonify(result)

    except Exception as e:
        return {"error": e.__str__()}


if __name__ == '__main__':
    app.run(debug=True)
