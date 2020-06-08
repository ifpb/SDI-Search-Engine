from multiprocessing import Process, Manager
from util import filter_result_of_dict


class AbstractService(object):
    def __init__(self, filter_spatial, filter_spatial_args, filter_temporal, filter_temporal_args):
        self.filter_spatial = filter_spatial
        self.filter_spatial_args = filter_spatial_args
        self.filter_temporal = filter_temporal
        self.filter_temporal_args = filter_temporal_args

    def find(self, filters):
        with Manager() as manager:
            spatial_process = None
            temporal_process = None

            if filters.__contains__('place_name'):
                print('filter spatial')
                query_spatial = manager.dict()
                exception_spatial = manager.dict()
                spatial_process = Process(target=self.filter_spatial,
                                          args=self.filter_spatial_args)
                print('start spatial process')
                spatial_process.start()
            if filters.__contains__('start_date') and filters.__contains__('end_date'):
                print('filter temporal')
                query_temporal = manager.dict()
                temporal_process = Process(target=self.filter_temporal,
                                           args=self.filter_temporal_args)
                print('start temporal process')
                temporal_process.start()
            if filters.__contains__('theme'):
                print('consulta com tema')

            if spatial_process is not None:
                spatial_process.join()
                print('join spatial process')

            if temporal_process is not None:
                temporal_process.join()
                print('join temporal process')

            if spatial_process is not None:
                if exception_spatial.keys().__contains__('exception'):
                    raise exception_spatial['exception']

            queries = []
            if spatial_process is not None:
                queries.append(query_spatial)
            if temporal_process is not None:
                queries.append(query_temporal)

            return filter_result_of_dict(queries)
