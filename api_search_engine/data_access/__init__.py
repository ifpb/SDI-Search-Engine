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
    result = engine.execute(f"SELECT nome, tipo, geom FROM place WHERE nome ILIKE '{place_name}'").fetchall()
    app_log.info("find place result: " + str(result[0]))
    return result[0]


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
         + 1 * (ST_Area(ST_Difference('{service_geometry}'::geometry, '{place_geometry}'::geometry)))
        + 1 * (ST_Area(ST_Difference('{place_geometry}'::geometry, '{service_geometry}'::geometry))) )
    ) as tversky
    """
    result = engine.execute(query).fetchall()[0]
    return result["tversky"]
