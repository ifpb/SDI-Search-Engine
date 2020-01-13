import traceback

import util
from sqlalchemy import create_engine
from data_access.DataUpdateException import DataUpdateException

'''
    Modulo de acesso e persistência de dados no banco de dados 
    Autor: 
        Leanderson Coelho
'''

# buscando configuração de log
log = util.getLogger()

# engine para conexão com banco de dados
try:
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/inde')
except Exception as e:
    traceback.print_exc()


def persistirCatalogo(dataFrame):
    try:
        dataFrame.to_sql(name='catalogo', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: catalogo')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em catalogo')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{dataFrame.tail(5)}')
        raise DataUpdateException()

def persistirRegistro(dataFrame):
    try:
        dataFrame.to_sql(name='registro', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: registro')
    except Exception as e:
        log.error('Falha ao salvar DataFrame em registro')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{dataFrame.tail(5)}')
        raise DataUpdateException()

def persistirServico(dataFrame):
    try:
        dataFrame.to_sql(name='servico', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: servico')
    except:
        log.error('Falha ao salvar DataFrame em servico')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{dataFrame.tail(5)}')
        raise DataUpdateException()

def persistirFeatureType(dataFrame):
    try:
        dataFrame.to_sql(name='feature_type', con=engine, if_exists='append', index=True, index_label='id')
        log.info('Nova tupla em: feature_type')
    except:
        log.error('Falha ao salvar DataFrame em registro')
        log.error(f'Detalhes: {e}')
        log.error(f'DataFrame:\n{dataFrame.tail(5)}')
        raise DataUpdateException()