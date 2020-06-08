from data_access.DataAccess import DataAccess


def retrieve_services(data):
    if data and data.__len__() > 0:
        services = []
        for s in DataAccess().retrieve_services(data):
            services.append(build_service(s))
        return services
    return []


def retrieve_features_types(data):
    if data and data.__len__() > 0:
        features = []
        for f in DataAccess().retrieve_features_types(data):
            features.append(build_feature_type(f))
        return features
    return []


def build_service(data):
    return {
        'id': data[0],
        'wfs_url': data[1],
        'wms_url': data[2],
        'service_processed': data[3],
        'title': data[4],
        'description': data[5],
        'publisher': data[6],
        'start_date': data[7],
        'end_date': data[8],
    }


def build_feature_type(data):
    return {
        'id': data[0],
        'title': data[1],
        'description': data[2],
        'keywords': data[3],
        'start_date': data[4],
        'end_date': data[5],
    }
