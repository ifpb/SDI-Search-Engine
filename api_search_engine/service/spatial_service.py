import data_access
import log
from request_status.multiple_choices import HttpMultipleChoices
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound
from service import MultipleChoices as mc
import time

""" Obtem o log padão da aplicação """
app_log = log.get_logger()

SIMILARITY_MIN = 0.0001


def find_place(place_name):
    """find for one place with associate locale"""
    place = data_access.find_place(place_name)
    if place is not None:
        if len(place) == 1:
            return place[0]
        else:
            app_log.info("more one places")
            e = mc.MultipleChoices()
            e.data = place
            raise e
    else:
        app_log.info("not find place")
        raise HttpNotFound


def find_place_in_level_service(place_name, is_place_id=False):
    """search for services with associate locale"""
    if not is_place_id:
        place = find_place(place_name)
    else:
        place = data_access.find_place_id(place_name)
        app_log.info("place by id")
    #
    all_services = data_access.find_all_services()
    result = {}
    if len(all_services) > 0:
        for service in all_services:
            service_round = build_service(service)
            # 1 verify if the service intersect
            if data_access.verify_intersect(service[0], place[2]):
                list_of_features = data_access.feature_types_of_service(service)
                if len(list_of_features) > 0:
                    # 2 verify the intersection with each feature type
                    features_intersects = intersection_with_place(list_of_features, place)
                    if len(features_intersects) > 0:
                        # 3 calculate the similarity between two geometry
                        service_round = services_with_similarity(features_intersects, place, service_round)
                        if service_round["quantity"] > 0:
                            service_round["similarity"] = service_round["sum_similarity"] / len(list_of_features)
                            app_log.info("Serviço relacionado similarity total: " +
                                         str(service_round["similarity"]) + " id: " + service_round["id"])
                            result[service_round["id"]] = service_round['similarity']
        app_log.info('quantidade final: '+str(len(result)))
        return result
    else:
        app_log.info("not find services")
        raise HttpNotContent


def find_place_in_level_feature_type(place_name, is_place_id=False):
    """search for features types with associate locale"""
    if not is_place_id:
        place = find_place(place_name)
    else:
        place = data_access.find_place_id(place_name)
        app_log.info("place by id")
    #
    all_services = data_access.find_all_services()
    if len(all_services) > 0:
        result = {}
        for service in all_services:
            if data_access.verify_intersect(service[0], place[2]):
                app_log.info('service id: ' + service[1])
                list_of_features = data_access.feature_types_of_service_id_geom(service)
                app_log.info('total de ft do service: ' + str(len(list_of_features)))
                if len(list_of_features) > 0:
                    features_intersects = intersection_with_place(list_of_features, place)
                    app_log.info('total de ft que intersectam com o place: ' + str(len(features_intersects)))
                    if len(features_intersects) > 0:
                        result = calculate_similarity_of_feature_type(features_intersects, place, result)
        app_log.info('quantidade final: '+str(len(result)))
        return result
    else:
        app_log.info("not find services")
        raise HttpNotContent


def services_with_similarity(features_intersects, place, service_round):
    """calculate the similarity between two geometry"""
    for feature in features_intersects:
        similarity = data_access.calcule_tversky(place[2], feature[0])
        if similarity > SIMILARITY_MIN:
            service_round["quantity"] += 1
            service_round["sum_similarity"] += similarity
            app_log.info("-------> similarity of feature: " + str(similarity))
            app_log.info("-------> feature_id: " + feature[1])
    return service_round


def intersection_with_place(list_of_features, place):
    """verify the intersection with each feature type"""
    features_intersects = []
    for feature in list_of_features:
        if data_access.verify_intersect(place[2], feature[0]) is True:
            features_intersects.append(feature)
    return features_intersects


def calculate_similarity_of_feature_type(features_intersects, place, result):
    """calculate the similarity between the place and feature type"""
    for feature in features_intersects:
        app_log.info('id of the feature: ' + feature[1])
        similarity = data_access.calcule_tversky(place[2], feature[0])
        if similarity > SIMILARITY_MIN:
            app_log.info("------> feature: " + feature[1] + " similarity: " + str(similarity))
            result[feature[1]] = similarity
    return result


def build_service(service):
    service_round = {
        "id": service[1],
        "quantity": 0,
        "similarity": 0,
        "sum_similarity": 0
    }
    return service_round


def build_feature_type(feature, similarity):
    feature = {
        "id": feature[1],
        "similarity": similarity,
        "title": feature[2],
        "name": feature[3],
        "description": feature[4],
        "keywords": feature[5],
        "service_id": feature[6]
    }
    return feature


def retrieve_all_places(places):
    """this"""
    choices = []
    for place in places:
        if place[1] == "MUNICÍPIO":
            # verify which UF contains this place
            uf = data_access.uf_contains_place(place[2])
            choices.append(build_city_place_for_choice(place, uf[0]))
        else:
            choices.append(build_uf_place_for_choice(place))
    return choices


def build_city_place_for_choice(place_info, uf):
    """this"""
    return {
        "id": place_info[3],
        "name": place_info[0],
        "UF": uf,
        "type": place_info[1]
    }


def build_uf_place_for_choice(place_info):
    """this"""
    return {
        "id": place_info[3],
        "name": place_info[0],
        "type": place_info[1]
    }
