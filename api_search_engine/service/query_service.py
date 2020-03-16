import data_access
import log


""" Obtem o log padão da aplicação """
app_log = log.get_logger()


def find_place_in_level_service(place_name):
    place = data_access.find_place(place_name)
    app_log.info(str(place[2]))
    all_services = data_access.find_all_services()
    similarity_list = []
    if len(all_services) > 0:
        for service in all_services:
            # place[ 2 ] = geom
            # service[ 6 ] = geom
            similarity = data_access.calcule_tversky(service[0], place[2])
            if similarity > 0:
                similarity_list.append({"service": {
                    "id": service[1],
                    "url": service[2],
                    "type": service[3],
                    "title": service[4],
                    "description": service[5],
                    "publisher": service[6]
                }, "similarity": similarity})
        app_log.info(similarity_list)
    else:
        app_log.info("not find services with similarity")
    return similarity_list
    # app_log.info(place)
