import data_access


def retrieve_services(data):
    services = []
    for s in data_access.retrieve_services(data):
        services.append(build_service(s))
    return services


def retrieve_features_types(data):
    features = []
    for f in data_access.retrieve_features_types(data):
        features.append(build_feature_type(f))
    return features


def build_service(data):
    return {
        'wfs_url': data[0],
        'wms_url': data[1],
        'service_processed': data[2],
        'title': data[3],
        'description': data[4],
        'publisher': data[5],
        'start_date': data[6],
        'end_date': data[7],
    }


def build_feature_type(data):
    return {
        'title': data[0],
        'description': data[1],
        'keywords': data[2],
        'start_date': data[3],
        'end_date': data[4],
    }
