from service import spatial_service, temporal_service
from multiprocessing import Process, Manager


def find(filters, params):
    with Manager() as manager:
        query_spatial = manager.dict()
        query_temporal = manager.dict()
        spatial_process = Process(target=spatial_service.find_place_in_level_feature_type,
                                  args=(filters['place_name'], query_spatial))
        temporal_process = Process(target=temporal_service.features_intersects_dates, args=(filters, query_temporal))
        FILTERS_LENGTH = 2
        if params.get('thematic'):
            print('tem thematic')
            FILTERS_LENGTH += 1

        spatial_process.start()
        temporal_process.start()
        temporal_process.join()
        spatial_process.join()

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
