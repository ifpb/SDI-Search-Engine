from service import spatial_service, temporal_service


def find(filters, params):
    FILTERS_LENGTH = 2
    if params.get('thematic'):
        print('tem thematic')
        FILTERS_LENGTH += 1
    query_spatial = spatial_service.find_place_in_level_feature_type(filters['place_name'])
    print(query_spatial)
    query_temporal = temporal_service.features_intersects_dates(filters)
    print(query_temporal)
    result = {}
    if FILTERS_LENGTH == 2:
        if query_spatial.__len__() >= query_temporal.__len__():
            for t in query_temporal:
                if query_spatial.__contains__(f'{t}'):
                    result[t] = (query_temporal[t] + query_spatial[t]) / 2
        else:
            for t in query_spatial:
                if query_temporal.__contains__(f'{t}'):
                    result[t] = (query_temporal[t] + query_spatial[t]) / 2
    else:
        raise Exception('Method not implemented')
    return result