import time

from service.temporal_service import TemporalService
from service.spatial_service import SpatialService
from service.thematic_service import ThematicService
from multiprocessing import Process, Manager
from util import filter_result_of_dict
import log

app_log = log.get_logger()


def find(filters, is_place_id=False):
    app_log.info(filters)
    with Manager() as manager:
        spatial_process = None
        temporal_process = None
        thematic_process = None

        if filters.__contains__('place_name') and filters['place_name'] != '':
            app_log.info('FEATURE TYPE SERVICE -> filter spatial')
            spatial_service = SpatialService()
            query_spatial = manager.dict()
            exception_spatial = manager.dict()
            spatial_process = Process(target=spatial_service.find_place_in_level_feature_typev2,
                                      args=(filters['place_name'], query_spatial, exception_spatial, is_place_id))
            app_log.info('FEATURE TYPE SERVICE -> start spatial process')
            spatial_process.start()
        if filters.__contains__('start_date') and filters['start_date'] != '' and filters.__contains__('end_date') and \
                filters['end_date'] != '':
            app_log.info('FEATURE TYPE SERVICE -> filter temporal')
            temporal_service = TemporalService()
            query_temporal = manager.dict()
            temporal_process = Process(target=temporal_service.features_intersects_dates,
                                       args=(filters, query_temporal))
            app_log.info('FEATURE TYPE SERVICE -> start temporal process')
            temporal_process.start()
        if filters.__contains__('theme') and filters['theme'] != '':
            app_log.info('FEATURE TYPE SERVICE -> consulta com tema')
            thematic_service = ThematicService()
            query_thematic = manager.dict()
            thematic_process = Process(target=thematic_service.search_in_level_feature_type,
                                       args=(filters['theme'], query_thematic))
            app_log.info('FEATURE TYPE SERVICE -> start thematic process')
            thematic_process.start()

        if spatial_process is not None:
            spatial_process.join()
            app_log.info('FEATURE TYPE SERVICE -> join spatial process')

        if temporal_process is not None:
            temporal_process.join()
            app_log.info('FEATURE TYPE SERVICE -> join temporal process')

        if thematic_process is not None:
            thematic_process.join()
            app_log.info('FEATURE TYPE SERVICE -> join thematic process')

        if spatial_process is not None:
            if exception_spatial.keys().__contains__('exception'):
                raise exception_spatial['exception']

        queries = []
        if spatial_process is not None:
            queries.append(query_spatial)
        if temporal_process is not None:
            queries.append(query_temporal)
        if thematic_process is not None:
            queries.append(query_thematic)

        return filter_result_of_dict(queries)


def similar_feature_type(feature_type_id):
    if feature_type_id is None:
        raise Exception('feature type id is invalid')
    app_log.info('feature type id: ' + str(feature_type_id))

    spatial_service = SpatialService()

    feature_type = spatial_service.retrieve_feature_type(feature_type_id)
    return find_by_bbox({
        'feature_type_id': feature_type_id,
        'xmin': feature_type[1],
        'ymin': feature_type[2],
        'xmax': feature_type[3],
        'ymax': feature_type[4],
        'geometry': feature_type[5],
        'theme': feature_type[0],
        'start_date': '',
        'end_date': ''
    }, True)


def find_by_bbox(filters, is_feature_type=False):
    app_log.info('FEATURE TYPE SERVICE -> find_by_bbox')

    if not is_feature_type:
        filters['geometry'] = None

    app_log.info(filters)
    with Manager() as manager:
        temporal_process = None
        thematic_process = None

        # SPATIAL FILTER IS REQUIRED
        spatial_service = SpatialService()
        query_spatial = manager.dict()
        exception_spatial = manager.dict()

        spatial_process = Process(target=spatial_service.find_feature_types_similar_to,
                                  args=(filters, query_spatial, exception_spatial))
        spatial_process.start()

        if filters.__contains__('start_date') and filters['start_date'] != '' and filters.__contains__('end_date') and \
                filters['end_date'] != '':
            app_log.info('FEATURE TYPE SERVICE -> filter temporal')
            temporal_service = TemporalService()
            query_temporal = manager.dict()
            temporal_process = Process(target=temporal_service.features_intersects_dates,
                                       args=(filters, query_temporal))
            app_log.info('FEATURE TYPE SERVICE -> start temporal process')
            temporal_process.start()
        if filters.__contains__('theme') and filters['theme'] != '':
            app_log.info('FEATURE TYPE SERVICE -> consulta com tema')
            thematic_service = ThematicService()
            query_thematic = manager.dict()
            thematic_process = Process(target=thematic_service.search_in_level_feature_type,
                                       args=(filters['theme'], query_thematic))
            app_log.info('FEATURE TYPE SERVICE -> start thematic process')
            thematic_process.start()

        spatial_process.join()
        app_log.info('FEATURE TYPE SERVICE -> join spatial process')

        if temporal_process is not None:
            temporal_process.join()
            app_log.info('FEATURE TYPE SERVICE -> join temporal process')

        if thematic_process is not None:
            thematic_process.join()
            app_log.info('FEATURE TYPE SERVICE -> join thematic process')

        if exception_spatial.keys().__contains__('exception'):
            raise exception_spatial['exception']

        queries = [query_spatial]
        if temporal_process is not None:
            queries.append(query_temporal)
        if thematic_process is not None:
            queries.append(query_thematic)

        result = filter_result_of_dict(queries)
        app_log.info(result)
        return result
