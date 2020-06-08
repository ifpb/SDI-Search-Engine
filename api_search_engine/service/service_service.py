from service.temporal_service import TemporalService
from service.spatial_service import SpatialService
from multiprocessing import Process, Manager
from util import filter_result_of_dict
import log

app_log = log.get_logger()


def find(filters, is_place_id=False):
    with Manager() as manager:
        spatial_process = None
        temporal_process = None

        if filters.__contains__('place_name') and filters['place_name'] != '':
            app_log.info('SERVICE of SERVICE -> filter spatial')
            spatial_service = SpatialService()
            query_spatial = manager.dict()
            exception_spatial = manager.dict()
            spatial_process = Process(target=spatial_service.find_place_in_level_service,
                                      args=(filters['place_name'], query_spatial, exception_spatial, is_place_id))
            app_log.info('SERVICE of SERVICE -> start spatial process')
            spatial_process.start()
        if filters.__contains__('start_date') and filters['start_date'] != '' and filters.__contains__('end_date') and \
                filters['end_date'] != '':
            app_log.info('SERVICE of SERVICE -> filter temporal')
            temporal_service = TemporalService()
            query_temporal = manager.dict()
            temporal_process = Process(target=temporal_service.services_intersects_dates,
                                       args=(filters, query_temporal))
            app_log.info('SERVICE of SERVICE -> start temporal process')
            temporal_process.start()
        if filters.__contains__('theme') and filters['theme'] != '':
            app_log.info('SERVICE of SERVICE -> consulta com tema')

        if spatial_process is not None:
            spatial_process.join()
            app_log.info('SERVICE of SERVICE -> join spatial process')

        if temporal_process is not None:
            temporal_process.join()
            app_log.info('SERVICE of SERVICE -> join temporal process')

        if spatial_process is not None:
            if exception_spatial.keys().__contains__('exception'):
                raise exception_spatial['exception']

        queries = []
        if spatial_process is not None:
            queries.append(query_spatial)
        if temporal_process is not None:
            queries.append(query_temporal)

        return filter_result_of_dict(queries)
