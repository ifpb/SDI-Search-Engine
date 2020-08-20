from data_access.DataAccess import DataAccess
import log
from request_status.not_content import HttpNotContent
from request_status.not_found import HttpNotFound
from service import MultipleChoices as mc


class SpatialService(object):

    def __init__(self):
        self.app_log = log.get_logger()
        self.SIMILARITY_MIN = 0.0001
        self.DataAccess = DataAccess()
        
    def __del__(self):
        self.app_log.info('SPATIAL SERVICE ->   delete SpatialService')
        self.DataAccess.close_engine_connections()

    def retrieve_feature_type(self, id):
        return self.DataAccess.retrieve_feature_type(id)

    def find_place(self, place_name):
        """find for one place with associate locale"""
        place = self.DataAccess.find_place(place_name)
        if place is not None:
            if len(place) == 1:
                return place[0]
            else:
                self.app_log.info('SPATIAL SERVICE -> more one places')
                e = mc.MultipleChoices()
                e.data = place
                raise e
        else:
            self.app_log.info('SPATIAL SERVICE -> not find place')
            raise HttpNotFound

    def find_place_in_level_service(self, place_name, data, exception, is_place_id=False):
        """search for services with associate locale"""
        try:
            if not is_place_id:
                place = self.find_place(place_name)
            else:
                place = self.DataAccess.find_place_id(place_name)
                self.app_log.info('SPATIAL SERVICE -> place by id')
            #
            all_services = self.DataAccess.find_all_services()
            if len(all_services) > 0:
                for service in all_services:
                    service_round = self.build_service(service)
                    # 1 verify if the service intersect
                    if self.DataAccess.verify_intersect(service[0], place[2]):
                        list_of_features = self.DataAccess.feature_types_of_service(service)
                        if len(list_of_features) > 0:
                            # 2 verify the intersection with each feature type
                            features_intersects = self.intersection_with_place(list_of_features, place)
                            if len(features_intersects) > 0:
                                # 3 calculate the similarity between two geometry
                                service_round = self.services_with_similarity(features_intersects, place, service_round)
                                if service_round["quantity"] > 0:
                                    service_round["similarity"] = service_round["sum_similarity"] / len(list_of_features)
                                    self.app_log.info('SPATIAL SERVICE ->Serviço relacionado similarity total: ' +
                                                      str(service_round["similarity"]) + ' id: ' + service_round["id"])
                                    data[service_round["id"]] = service_round['similarity']
                self.app_log.info('SPATIAL SERVICE ->   quantidade final: ' + str(len(data)))
            else:
                self.app_log.info('SPATIAL SERVICE -> not find services')
                raise HttpNotContent
        except Exception as e:
            exception['exception'] = e

    def find_place_in_level_servicev2(self, place_name, data, exception, is_place_id=False):
        try:
            if not is_place_id:
                place = self.find_place(place_name)
            else:
                place = self.DataAccess.find_place_id(place_name)
                self.app_log.info('SPATIAL SERVICE -> place by id')
            #
            result = self.DataAccess.services_with_intersects_and_similarityv2(place)
            for r in result:
                data[r[0]] = r[1]
            self.app_log.info('SPATIAL SERVICE -> quantidade final: ' + str(len(data)))
        except Exception as e:
           exception['exception'] = e

    def find_place_in_level_feature_type(self, place_name, data, exception, is_place_id=False):
        """search for features types with associate locale"""
        try:
            if not is_place_id:
                place = self.find_place(place_name)
            else:
                place = self.DataAccess.find_place_id(place_name)
                # self.app_log.info('SPATIAL SERVICE -> place by id')
            all_services = self.DataAccess.find_all_services()
            if len(all_services) > 0:
                for service in all_services:
                    if self.DataAccess.verify_intersect(service[0], place[2]):
                        # self.app_log.info('SPATIAL SERVICE ->   service id: ' + service[1])
                        list_of_features = self.DataAccess.feature_types_of_service_id_geom(service)
                        # self.app_log.info('SPATIAL SERVICE ->   total de ft do service: ' + str(len(list_of_features)))
                        if len(list_of_features) > 0:
                            features_intersects = self.intersection_with_place(list_of_features, place)
                            # self.app_log.info(
                            #     'total de ft que intersectam com o place: ' + str(len(features_intersects)))
                            if len(features_intersects) > 0:
                                self.calculate_similarity_of_feature_type(features_intersects, place, data)
                self.app_log.info('SPATIAL SERVICE ->   quantidade final: ' + str(len(data)))
            else:
                self.app_log.info('SPATIAL SERVICE -> not find services')
                raise HttpNotContent
        except Exception as e:
            exception['exception'] = e

    def find_place_in_level_feature_typev2(self, place_name, data, exception, is_place_id=False):
        try:
            self.app_log.info('FIND PLACE')
            if not is_place_id:
                place = self.find_place(place_name)
            else:
                place = self.DataAccess.find_place_id(place_name)
            self.app_log.info('PLACE LOADED')
            result = self.DataAccess.features_with_intersects_and_similarityv2(place[5], place[6], place[7], place[8], place[2])
            for r in result:
                data[r[0]] = r[1]
        except Exception as e:
            exception['exception'] = e

    def find_feature_types_similar_to(self, feature_type, data, exception):
        try:
            result = self.DataAccess.features_with_intersects_and_similarityv2(feature_type['xmin'], feature_type['ymin'],
                                                                               feature_type['xmax'], feature_type['ymax'],
                                                                               feature_type['geometry'])
            if feature_type.keys().__contains__('feature_type_id'):
                for r in result:
                    if r[0] != feature_type['feature_type_id']:
                        data[r[0]] = r[1]
            else:
                for r in result:
                    data[r[0]] = r[1]
        except Exception as e:
            exception['exception'] = e

    def services_with_similarity(self, features_intersects, place, service_round):
        """calculate the similarity between two geometry"""
        for feature in features_intersects:
            similarity = self.DataAccess.calcule_tversky(place[2], feature[0])
            if similarity > self.SIMILARITY_MIN:
                service_round["quantity"] += 1
                service_round["sum_similarity"] += similarity
                self.app_log.info('SPATIAL SERVICE -> -------> similarity of feature: ' + str(similarity))
                self.app_log.info('SPATIAL SERVICE -> -------> feature_id: ' + feature[1])
        return service_round

    def intersection_with_place(self, list_of_features, place):
        """verify the intersection with each feature type"""
        features_intersects = []
        for feature in list_of_features:
            if self.DataAccess.verify_intersect(place[2], feature[0]) is True:
                features_intersects.append(feature)
        return features_intersects

    def calculate_similarity_of_feature_type(self, features_intersects, place, data):
        """calculate the similarity between the place and feature type"""
        for feature in features_intersects:
            # self.app_log.info('SPATIAL SERVICE ->   id of the feature: ' + feature[1])
            similarity = self.DataAccess.calcule_tversky(place[2], feature[0])
            if similarity > self.SIMILARITY_MIN:
                # self.app_log.info('SPATIAL SERVICE -> ------> feature: ' + feature[1] + ' similarity: ' + str(similarity))
                data[feature[1]] = similarity

    def build_service(self, service):
        service_round = {
            "id": service[1],
            "quantity": 0,
            "similarity": 0,
            "sum_similarity": 0
        }
        return service_round

    def build_feature_type(self, feature, similarity):
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

    def retrieve_all_places(self, places):
        """this"""
        choices = []
        for place in places:
            if place[1] == "MUNICÍPIO":
                # verify which UF contains this place
                uf = self.DataAccess.uf_contains_place(place[2])
                choices.append(self.build_city_place_for_choice(place, uf[0]))
            else:
                choices.append(self.build_uf_place_for_choice(place))
        return choices

    def build_city_place_for_choice(self, place_info, uf):
        """this"""
        return {
            "id": place_info[3],
            "name": place_info[0],
            "UF": uf,
            "type": place_info[1]
        }

    def build_uf_place_for_choice(self, place_info):
        """this"""
        return {
            "id": place_info[3],
            "name": place_info[0],
            "type": place_info[1]
        }
