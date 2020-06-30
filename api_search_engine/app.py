from flask import Flask, request, make_response, jsonify
import log
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound
from service import MultipleChoices as ss, feature_type_service, service_service, retrieve_service
from service.spatial_service import SpatialService
from service.temporal_service import TemporalService
import json
from flask_cors import cross_origin
from multiprocessing import Manager

build_json = (lambda v: json.dumps(v, default=lambda o: o.__dict__))

app = Flask(__name__)

""" Obtem o log padão da aplicação """
app_log = log.get_logger()


@app.route('/find-place/level-service/', methods=['POST'])
@cross_origin()
def find_place():
    try:
        spatial_service = SpatialService()
        data = request.get_json()
        place_name = data['place_name']
        app.logger.debug('request find-place: ' + place_name)
        list_services = spatial_service.find_place_in_level_service(place_name)
        return jsonify(list_services)
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except ss.MultipleChoices as e:
        return jsonify(spatial_service.retrieve_all_places(e.data)), e.code
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/find-place/level-feature-type/', methods=['POST'])
@cross_origin()
def find_place_feature_types():
    try:
        spatial_service = SpatialService()
        data = request.get_json()
        place_name = data['place_name']
        app.logger.debug('request find-place: ' + place_name)
        return jsonify(spatial_service.find_place_in_level_feature_type(place_name))
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except ss.MultipleChoices as e:
        return jsonify(spatial_service.retrieve_all_places(e.data)), 300
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/find-place/choice', methods=['POST'])
@cross_origin()
def by_choice_find_place():
    try:
        with Manager() as manager:
            data_manager = manager.dict()
            exception = manager.dict()
            spatial_service = SpatialService()
            data = request.get_json()
            place = data["choice"]
            app_log.info(str(place["id"]) + place["name"])
            level = request.args.get("level")
            if level == "SERVICE":
                app_log.info("choice in level of the service")
                spatial_service.find_place_in_level_servicev2(place["id"], data_manager, exception, is_place_id=True)
            else:
                app_log.info("choice in level of the feature type")
                spatial_service.find_place_in_level_feature_typev2(place["id"], data_manager, exception, is_place_id=True)
            if exception.keys().__contains__('exception'):
                raise exception['exception']
            return jsonify(data_manager)
    except Exception as e:
            app_log.info(e.__str__())
            return make_response(), 400


@app.route('/find-date/level-feature-type', methods=['POST'])
@cross_origin()
def find_by_interval_date():
    try:
        temporal_service = TemporalService()
        data = request.get_json()
        return jsonify(temporal_service.features_intersects_dates(data))
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/find/feature-type', methods=['POST'])
@cross_origin()
def find_feature_types():
    try:
        is_place_id = request.args.get("isPlaceId")
        if is_place_id is not None:
            if is_place_id == 'true':
                is_place_id = True
            else:
                is_place_id = False
        result = feature_type_service.find(request.get_json(), is_place_id=is_place_id)
        return jsonify(result)
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except ss.MultipleChoices as e:
        spatial_service = SpatialService()
        return jsonify(spatial_service.retrieve_all_places(e.data)), 300
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/find/service', methods=['POST'])
@cross_origin()
def find_services():
    try:
        is_place_id = request.args.get("isPlaceId")
        if is_place_id is not None:
            if is_place_id == 'true':
                is_place_id = True
            else:
                is_place_id = False
        result = service_service.find(request.get_json(), is_place_id=is_place_id)
        return jsonify(result)
    except HttpNotFound as e:
        return make_response(jsonify(e.message), e.code)
    except ss.MultipleChoices as e:
        spatial_service = SpatialService()
        return jsonify(spatial_service.retrieve_all_places(e.data)), 300
    except HttpNotContent as e:
        return make_response(jsonify(e.message), e.code)
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/retrieve/service', methods=['POST'])
@cross_origin()
def retrieve_services():
    try:
        data = request.get_json()
        return jsonify(retrieve_service.retrieve_services(data))
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


@app.route('/retrieve/feature-type', methods=['POST'])
@cross_origin()
def retrieve_features_types():
    try:
        data = request.get_json()
        return jsonify(retrieve_service.retrieve_features_types(data))
    except Exception as e:
        app_log.info(e.__str__())
        return make_response(), 400


if __name__ == '__main__':
    app.run(debug=True)
