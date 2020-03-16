from flask import Flask, Response, url_for, render_template, request, Response, make_response, jsonify
from service import query_service
import json
from flask_cors import CORS, cross_origin

build_json = (lambda v: json.dumps(v, default=lambda o: o.__dict__))

app = Flask(__name__)


@app.route('/find-place/level-service/', methods=['GET', 'POST'])
@cross_origin()
def find_place():
    data = request.get_json()
    place_name = data['place-name']
    app.logger.debug('request find-place: ' + place_name)
    list_services = query_service.find_place_in_level_service(place_name)
    # return build_json(list_services)
    return jsonify(list_services)


if __name__ == '__main__':
    app.run(debug=True)
