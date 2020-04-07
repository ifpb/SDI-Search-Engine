from werkzeug.http import HTTP_STATUS_CODES

import data_access
import log
from request_status.multiple_choices import HttpMultipleChoices
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound

""" Obtem o log padão da aplicação """
app_log = log.get_logger()

SIMILARITY_MIN = 0.0001


def find_place_in_level_service(place_name):
    """search for services with associate locale"""
    place = data_access.find_place(place_name)
    if place is not None:
        if len(place) == 1:
            place = place[0]
            all_services = data_access.find_all_services()
            result = []
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
                                                 str(service_round["similarity"]) + " quantidade: " +
                                                 str(service_round["quantity"]) + " título " + service_round["title"])
                                    result.append(service_round)
                return result
            else:
                app_log.info("not find services")
                raise HttpNotContent
        else:
            app_log.info("more one places")
            raise HttpMultipleChoices
    else:
        app_log.info("not find place")
        raise HttpNotFound


def find_place_in_level_feature_type(place_name):
    """search for features types with associate locale"""
    place = data_access.find_place(place_name)
    if place is not None:
        if len(place) == 1:
            place = place[0]
            all_services = data_access.find_all_services()
            if len(all_services) > 0:
                for service in all_services:
                    result = []
                    if data_access.verify_intersect(service[0], place[2]):
                        list_of_features = data_access.feature_types_of_service_all_data(service)
                        if len(list_of_features) > 0:
                            features_intersects = intersection_with_place(list_of_features, place)
                            if len(features_intersects) > 0:
                                result = calcule_similarity_of_feature_type(features_intersects, place)
                    return result
            else:
                app_log.info("not find services")
                raise HttpNotContent
        else:
            app_log.info("more one places")
            raise HttpMultipleChoices
    else:
        app_log.info("not find place")
        raise HttpNotFound


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


def calcule_similarity_of_feature_type(features_intersects, place):
    """calculate the similarity between the place and feature type"""
    features = []
    for feature in features_intersects:
        similarity = data_access.calcule_tversky(place[2], feature[0])
        if similarity > SIMILARITY_MIN:
            app_log.info("------> feature: " + feature[1] + " similarity: " + str(similarity))
            features.append(build_feature_type(feature, similarity))
    return features



def build_service(service):
    service_round = {
        "id": service[1],
        "url": service[2],
        "type": service[3],
        "title": service[4],
        "description": service[5],
        "publisher": service[6],
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
        "service_id": feature[6],
        "bounding_box_xmin": feature[7],
        "bounding_box_ymin": feature[8],
        "bounding_box_xmax": feature[9],
        "bounding_box_ymax": feature[10]
    }
    return feature

