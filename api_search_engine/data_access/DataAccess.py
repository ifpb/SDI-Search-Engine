from sqlalchemy import create_engine
import log
import data_access


class DataAccess(object):
    def __init__(self, _engine=None):
        self.app_log = log.get_logger()
        self.app_log.info('DataAccess -> new DataAccess')
        if _engine is None:
            self._engine = data_access.create_engine()
        self._app_log = log.get_logger()

    def close_engine_connections(self):
        self.app_log.info('DataAccess -> close engine DataAccess')
        self._engine.dispose()

    def find_place(self, place_name):
        result = self._engine.execute(
            f"SELECT nome, tipo, geom, gid FROM place WHERE nome ILIKE '{place_name}'").fetchall()
        if len(result) > 0:
            if len(result) > 1:
                self._app_log.info("DataAccess -> existe mais de um!")
                return result
            self._app_log.info("DataAccess -> find place result: " + result[0][0] + " - " + result[0][1])
            return result
        else:
            return None

    def find_place_id(self, place_id):
        result = self._engine.execute(f"SELECT nome, tipo, geom, gid FROM place WHERE gid = {place_id}").fetchall()
        if len(result) > 0:
            if len(result) > 1:
                self._app_log.info("DataAccess -> existe mais de um!")
                return result
            self._app_log.info("DataAccess -> find place result: " + result[0][0] + " - " + result[0][1])
            return result[0]
        else:
            return None

    def find_services_contains_place(self, place_geometry):
        query = f"""
        select * from service
        where ST_Contains(geometry, '{place_geometry}')
        """
        result = self._engine.execute(query).fetchall()
        self._app_log.info(result[0])

    def find_all_services(self):
        query = """
            SELECT geometry, id FROM service WHERE geometry is not null 
        """
        result = self._engine.execute(query).fetchall()
        return result

    def calcule_tversky(self, service_geometry, place_geometry):
        query = f"""
        SELECT (
            (ST_Area(ST_Intersection('{service_geometry}'::geometry, '{place_geometry}'::geometry)))
            /
            ( ST_Area(ST_Intersection('{service_geometry}'::geometry, '{place_geometry}'::geometry))
             + 0.5 * (ST_Area(ST_Difference('{service_geometry}'::geometry, '{place_geometry}'::geometry)))
            + 0.5 * (ST_Area(ST_Difference('{place_geometry}'::geometry, '{service_geometry}'::geometry))) )
        ) as tversky
        """
        result = self._engine.execute(query).fetchall()[0]
        return result["tversky"]

    def verify_intersect(self, geometry1, geometry2):
        query = f"SELECT ST_Intersects('{geometry1}'::geometry, '{geometry2}'::geometry)"
        result = self._engine.execute(query).fetchall()[0]
        return result[0]

    def verify_intersect_bbox(self, geometry1, feature):
        query = f"""
            SELECT ST_Intersects('{geometry1}'::geometry, 
            ST_MakeEnvelope({feature[0]}, {feature[1]}, {feature[2]}, {feature[3]}))
        """
        result = self._engine.execute(query).fetchall()[0]
        return result[0]

    def feature_types_of_service(self, service):
        query = f"""
                SELECT geometry as geom, id 
                from feature_type ft WHERE ft.service_id ilike '{service[1]}'
            """
        return self._engine.execute(query).fetchall()

    def feature_types_of_service_all_data(self, service):
        query = f"""
                SELECT geometry as geom, id, title, name, description, keywords, service_id 
                from feature_type ft WHERE ft.service_id ilike '{service[1]}'
            """
        return self._engine.execute(query).fetchall()

    def feature_types_of_service_id_geom(self, service):
        query = f"""
                SELECT geometry as geom, id from feature_type ft WHERE ft.service_id ilike '{service[1]}'
            """
        return self._engine.execute(query).fetchall()

    def service_id_dates(self):
        query = f"""
                SELECT id, start_date, end_date from service
            """
        return self._engine.execute(query).fetchall()

    def uf_contains_place(self, place):
        query = f"""
            SELECT nome FROM place WHERE ST_Contains(geom::geometry, '{place}'::geometry) 
            and tipo ilike 'UF'
        """
        result = self._engine.execute(query).fetchall()
        return result[0]

    def feature_type_id_dates(self):
        query = """
            SELECT id, start_date, end_date FROM feature_type
        """
        return self._engine.execute(query).fetchall()

    def retrieve_services(self, services):
        query = """
            SELECT id, wfs_url, wms_url, service_processed, title, description, publisher, start_date, end_date FROM SERVICE WHERE 
        """
        for s in services:
            query += f"id ilike '{s}' or "
        query = query[0:-4]
        return self._engine.execute(query).fetchall()

    def retrieve_features_types(self, features):
        query = """
                SELECT id, title, description, keywords, start_date, end_date FROM feature_type WHERE 
            """
        for f in features:
            query += f"id ilike '{f}' or "
        query = query[0:-4]
        return self._engine.execute(query).fetchall()
