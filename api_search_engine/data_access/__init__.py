from sqlalchemy import create_engine
import log
from model.service import Service

"""
    Classe responsável por acessar os dados disponível no banco da aplicação
"""

""" Obtem o log padão da aplicação """
app_log = log.get_logger()

try:
    """ Cria uma conexão com o banco de dados """
    engine = create_engine('postgresql://postgres:postgres@localhost:5433/inde_database')
except Exception as e:
    raise


def find_place(place_name):
    result = engine.execute(f"SELECT nome, tipo, geom, gid FROM place WHERE nome ILIKE '{place_name}'").fetchall()
    if len(result) > 0:
        if len(result) > 1:
            app_log.info("existe mais de um!")
            return result
        app_log.info("find place result: " + result[0][0] + " - " + result[0][1])
        return result
    else:
        return None


def find_place_id(place_id):
    result = engine.execute(f"SELECT nome, tipo, geom, gid FROM place WHERE gid = {place_id}").fetchall()
    if len(result) > 0:
        if len(result) > 1:
            app_log.info("existe mais de um!")
            return result
        app_log.info("find place result: " + result[0][0] + " - " + result[0][1])
        return result[0]
    else:
        return None



# only for test
def find_services_contains_place(place_geometry):
    query = f"""
    select * from service
    where ST_Contains(ST_MakeEnvelope(bounding_box_xmin::float, bounding_box_ymin::float,
    bounding_box_xmax::float, bounding_box_ymax::float), '{place_geometry}')
    """
    result = engine.execute(query).fetchall()
    app_log.info(result[0])


def find_all_services():
    query = """
        SELECT ST_MakeEnvelope(bounding_box_xmin::float, bounding_box_ymin::float,
        bounding_box_xmax::float, bounding_box_ymax::float),
        id, url, type, title, description, publisher from service 
        WHERE bounding_box_xmax not ilike '' and
			bounding_box_ymin not ilike '' and
			bounding_box_xmax not ilike '' and
			bounding_box_ymax not ilike '' 
    """
    result = engine.execute(query).fetchall()
    list_all_services = []
    if len(result) > 0:
        for s in result:
            list_all_services.append((s[0], s[1], s[2], s[3], s[4], s[5], s[6]))
    return list_all_services


def calcule_tversky(service_geometry, place_geometry):
    query = f"""
    SELECT (
        (ST_Area(ST_Intersection('{service_geometry}'::geometry, '{place_geometry}'::geometry)))
        /
        ( ST_Area(ST_Intersection('{service_geometry}'::geometry, '{place_geometry}'::geometry))
         + 0.5 * (ST_Area(ST_Difference('{service_geometry}'::geometry, '{place_geometry}'::geometry)))
        + 0.5 * (ST_Area(ST_Difference('{place_geometry}'::geometry, '{service_geometry}'::geometry))) )
    ) as tversky
    """
    result = engine.execute(query).fetchall()[0]
    return result["tversky"]


def verify_intersect(geometry1, geometry2):
    query = f"SELECT ST_Intersects('{geometry1}'::geometry, '{geometry2}'::geometry)"
    result = engine.execute(query).fetchall()[0]
    return result[0]


def verify_intersect_bbox(geometry1, feature):
    query = f"""
        SELECT ST_Intersects('{geometry1}'::geometry, 
        ST_MakeEnvelope({feature[0]}, {feature[1]}, {feature[2]}, {feature[3]}))
    """
    result = engine.execute(query).fetchall()[0]
    return result[0]


def feature_types_of_service(service):
    query = f"""
            SELECT ST_MakeEnvelope(
            bounding_box_xmin::float, bounding_box_ymin::float,
            bounding_box_xmax::float, bounding_box_ymax::float
            ) as geom, id 
            from feature_type ft WHERE ft.service_id ilike '{service[1]}'
        """
    return engine.execute(query).fetchall()


def feature_types_of_service_all_data(service):
    query = f"""
            SELECT ST_MakeEnvelope(
            bounding_box_xmin::float, bounding_box_ymin::float,
            bounding_box_xmax::float, bounding_box_ymax::float
            ) as geom, id, title, name, description, keywords, service_id,
            bounding_box_xmin, bounding_box_ymin, bounding_box_xmax, bounding_box_ymax 
            from feature_type ft WHERE ft.service_id ilike '{service[1]}'
        """
    return engine.execute(query).fetchall()


def uf_contains_place(place):
    query = f"""
        SELECT nome FROM place WHERE ST_Contains(geom::geometry, '{place}'::geometry) 
        and tipo ilike 'UF'
    """
    result = engine.execute(query).fetchall()
    return result[0]
