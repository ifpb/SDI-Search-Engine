import data_access
import log

""" Obtem o log padão da aplicação """
app_log = log.get_logger()


def find_place_in_level_service(place_name):
    place = data_access.find_place(place_name)
    if place is not None:
        app_log.info(str(place[2]))
        all_services = data_access.find_all_services()
        result = []
        if len(all_services) > 0:
            for service in all_services:
                service_round = {
                    "id": service[1],
                    "url": service[2],
                    "type": service[3],
                    "title": service[4],
                    "description": service[5],
                    "publisher": service[6],
                    "quantity": 0
                }
                # 1 verify if the service intersect
                if data_access.verify_intersect(service[0], place[2]):
                    # 2 verify the intersection with each feature type
                    list_of_features = data_access.feature_types_of_service(service)
                    if len(list_of_features) > 0:
                        features_intersects = []
                        for feature in list_of_features:
                            if feature[1] == '9e2e6b90-0392-4bcb-8f47-100cbd3876e6':
                                print("")
                            if data_access.verify_intersect(place[2], feature[0]) is True:
                                features_intersects.append(feature)
                        # 3 calculate the similarity between two geometry
                        if len(features_intersects) > 0:
                            for feature in features_intersects:
                                similarity = data_access.calcule_tversky(place[2], feature[0])
                                if similarity > 0.001:
                                    service_round["quantity"] += 1
                            if service_round["quantity"] > 0:
                                app_log.info("Serviço relacionado " + service_round["title"] + " quantidade: "
                                             + str(service_round["quantity"]))
                                result.append(service_round)
            return result
        else:
            app_log.info("not find services")
    return {"error": "place not found"}
    # app_log.info(place)


def test_find_services():
    all_services = data_access.find_all_services()
    print("kappa")
