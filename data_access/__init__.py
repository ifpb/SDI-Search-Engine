import traceback

import util
from sqlalchemy import create_engine
from data_access.DataUpdateException import DataUpdateException
from data_access.NotFoundServicesId import NotFoundServicesId
from pandas import read_sql_query

'''
    Modulo de acesso e persistência de dados no banco de dados 
    Autor: 
        Leanderson Coelho
'''

util.log_with_file(logWithFile=False)
''' Log com as configurações padroes '''
log = util.get_logger()

# engine para conexão com banco de dados
try:
    engine = create_engine('postgresql://postgres:postgres@localhost:5433/inde_database')
except:
    traceback.print_exc()


def persist_catalogue(data_frame):
    try:
        data_frame.to_sql(name='catalogue', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: catalogo')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em catalogo')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{data_frame.tail(5)}')
        raise DataUpdateException()


def persist_register(data_frame):
    try:
        data_frame.to_sql(name='register', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: registro')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em registro')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{data_frame.tail(5)}')
        raise DataUpdateException()


def persist_service(data_frame):
    try:
        data_frame.to_sql(name='service', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: servico')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em servico')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{data_frame.tail(5)}')
        raise DataUpdateException()


def persist_feature_type(data_frame):
    try:
        data_frame.to_sql(name='feature_type', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: feature_type')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em registro')
        log.error(f'Detalhes: {e}')
        print(data_frame)
        log.error(f'DataFrame:\n{data_frame.tail(5)}')
        raise DataUpdateException()


def find_all_services_id():
    services_id = engine.execute(
        "select ft.service_id, count(*) as qtd from feature_type ft group by ft.service_id order by qtd").fetchall()
    if len(services_id) > 0:
        list_services_id = []
        for service in services_id:
            list_services_id.append(service[0])
        return list_services_id
    else:
        raise NotFoundServicesId()


def create_bounding_box_of_service(service_id):
    sql = f"""
    select ST_Extent(p.geom) from place p, (
		select bounding_box_xmin as xmin, bounding_box_ymin as ymin, bounding_box_xmax as xmax,
		 bounding_box_ymax as ymax from feature_type ft where service_id ilike '{service_id}'
	) as bbox 
	where p.tipo ilike 'município' and
	 ST_Intersects(p.geom, ST_MakeEnvelope(bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax))
    """
    bbox = engine.execute(sql).fetchall()
    return util.bounding_box_from_tuple(bbox)


def update_service(service_id, bbox):
    try:
        result = engine.execute(f"UPDATE service SET bounding_box_xmin = {bbox[0]}, bounding_box_ymin = {bbox[1]},"
                                f"bounding_box_xmax = {bbox[2]}, bounding_box_ymax = {bbox[3]} "
                                f"WHERE id ilike '{service_id}'")
        return result
    except Exception as e:
        raise

