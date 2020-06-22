import traceback
from owslib.csw import CatalogueServiceWeb
from pandas import DataFrame
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from requests import ConnectTimeout, ReadTimeout

import tematic
import util
import data_access
import uuid
import geometry_data
import datetime

# turn off future warnings
import warnings

import tagging_temporal

warnings.simplefilter(action='ignore', category=FutureWarning)

''' Log com as configurações padroes '''
log = util.get_logger()


TYPE_SERVICE = 1


def find_date(data, type=1):
    # search for dates in text
    if data['title'] is not None:
        result = tagging_temporal.find_date(data['title'])
        if result is None:
            if data['description'] is not None:
                result = tagging_temporal.find_date(data['description'])
                if result is not None:
                    log.info('TAGGING - date in description')
                    log.info(str(result['start_date']) + " - " + str(result['end_date']))
                    data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
                    data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
                else:
                    if type != 1:
                        if data['keywords'] is not None:
                            result = tagging_temporal.find_date(data['keywords'])
                            if result is not None:
                                log.info('TAGGING - date in keywords')
                                log.info(str(result['start_date']) + " - " + str(result['end_date']))
                                data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
                                data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
                            else:
                                log.info('TAGGING - feature type without date')
        else:
            log.info('TAGGING - date in title')
            log.info(str(result['start_date']) + " - " + str(result['end_date']))
            data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
            data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
    return data


def find_date_in_service_metadata(service_date, date_attribute):
    result = tagging_temporal.find_date(date_attribute)
    if result is not None:
        service_date['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
        service_date['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
    return service_date


def persist_feature_type(content, service_description, service_id):
    '''Percorre todos as feições do serviço para armazenar no banco'''
    try:
        all_description = ''
        features_solr_docs = []
        data = {
            'title': '',
            'name': '',
            'description': '',
            'keywords': '',
            'service_id': service_id,
            'start_date': None,
            'end_date': None,
            'geometry': '',
            'area': None
        }
        columns = [
            'title', 'name', 'description', 'keywords', 'service_id', 'geometry', 'start_date', 'end_date', 'area'
        ]
        log.info("quantidade de ft: " + str(len(content)))
        for featureType in content:
            feature_description = ''
            feature_type_id = uuid.uuid4()
            data['title'] = util.process_escape_character(content[featureType].title)
            data['name'] = util.process_escape_character(featureType)
            if content[featureType].keywords is not None:
                data['keywords'] = util.process_escape_character(
                    ','.join(content[featureType].keywords))
            data['description'] = util.process_escape_character(content[featureType].abstract)
            data = find_date(data)
            if not data_access.exists_feature_type(data):
                # tematic index
                feature_description = util.build_string_for_solr([data['title'], data['description'], data['keywords']])
                all_description += feature_description
                feature_description += service_description
                features_solr_docs.append(tematic.build_doc_solr_feature_type(feature_description, feature_type_id))

                if content[featureType].boundingBox is not None:
                    data['geometry'] = data_access.create_geometry(
                        content[featureType].boundingBox[0],
                        content[featureType].boundingBox[1],
                        content[featureType].boundingBox[2],
                        content[featureType].boundingBox[3])
                    data['area'] = data_access.geometry_area(data['geometry'])
                log.info(data)
                df = DataFrame(data=data, columns=columns, index=[feature_type_id])
                data_access.persist_feature_type(df)
            else:
                log.info('exists feature-> name: ' + data['name'])
        tematic.add_documents_feature_type(features_solr_docs)
        return all_description
    except Exception as e:
        raise


def persist_wms_service(url_record, record, catalogue_id, url_wfs=None):
    '''Persiste no banco informações sobre um WMS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wms = WebMapService(url_record)
        if len(wms.contents) > 0:
            '''Só persisti o registro caso a requisição para o serviço de certo'''
            register_id = persist_register(record, catalogue_id)
            columns = ['wfs_url', 'wms_url', 'service_processed',
                       'title', 'description', 'publisher', 'register_id', 'geometry', 'start_date', 'end_date', 'area']
            data = {
                'wms_url': wms.url,
                'service_processed': 'OGC:WMS',
                'title': util.process_escape_character(record.title),
                'description': util.process_escape_character(record.abstract),
                'publisher': util.process_escape_character(
                    wms.provider.contact.organization),
                'register_id': register_id,
                'start_date': None,
                'end_date': None,
                'area': None
            }
            if url_wfs is not None:
                data['wfs_url'] = url_wfs
            if dir(wms.provider).__contains__('contact') and dir(wms.provider.contact).__contains__('organization'):
                data['publisher'] = util.process_escape_character(
                    wms.provider.contact.organization)
            elif record.publisher is not None:
                data['publisher'] = util.process_escape_character(record.publisher)
            else:
                data['publisher'] = None
            data = find_date(data, TYPE_SERVICE)
            if data['start_date'] and data['end_date'] is None:
                data = find_date_in_service_metadata(data, record.date)
            service_id = uuid.uuid4()
            # tematic index
            service_description = util.build_string_for_solr(
                [data['title'], data['description'], data['publisher']]
            )
            service_description += persist_feature_type(wms.contents, service_description, service_id.__str__())
            tematic.add_document_service(service_description, service_id)

            df = DataFrame(data=data, columns=columns, index=[service_id])
            data_access.persist_service(df)
            geometry_data.create_envelop_of_service(service_id)
        else:
            log.info('serviço sem feature types')
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persist_wfs_service(url_record, record, catalogue_id):
    '''Persiste no banco informações sobre um WFS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wfs = WebFeatureService(url_record)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        register_id = persist_register(record, catalogue_id)
        columns = ['wfs_url', 'wms_url', 'service_processed',
                   'title', 'description', 'publisher', 'register_id', 'start_date', 'end_date', 'geometry', 'area']
        data = {
            'wfs_url': wfs.url,
            'service_processed': 'OGC:WFS',
            'title': util.process_escape_character(record.title),
            'description': util.process_escape_character(record.abstract),
            'register_id': register_id,
            'start_date': None,
            'end_date': None,
            'area': None
        }
        '''Verificando se existe os atributos de publisher'''
        if dir(wfs.provider).__contains__('contact') and dir(wfs.provider.contact).__contains__('organization'):
            data['publisher'] = util.process_escape_character(
                wfs.provider.contact.organization)
        elif record.publisher is not None:
            data['publisher'] = util.process_escape_character(record.publisher)
        else:
            data['publisher'] = None
        data = find_date(data, TYPE_SERVICE)
        if data['start_date'] and data['end_date'] is None:
            data = find_date_in_service_metadata(data, record.date)
        service_id = uuid.uuid4()
        # tematic index
        service_description = util.build_string_for_solr(
            [data['title'], data['description'], data['publisher']]
        )
        service_description += persist_feature_type(wfs.contents, service_description, service_id.__str__())
        tematic.add_document_service(service_description, service_id)

        df = DataFrame(data=data, columns=columns, index=[service_id])
        data_access.persist_service(df)
        geometry_data.create_envelop_of_service(service_id)
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persist_register(register, catalogue_id):
    '''Persisti um novo registro no banco'''
    try:
        log.info('Coleta de dados do registro')
        columns = ['title', 'publisher', 'creation_data',
                   'modification_data', 'description', 'keywords', 'catalogo_id']
        keywords = None
        if register.subjects is not None:
            words = []
            for subject in register.subjects:
                if subject is not None:
                    words.append(subject)
            keywords = ','.join(words)
        data = {
            'title': util.process_escape_character(register.title),
            'publisher': util.process_escape_character(register.publisher),
            'creation_data': register.created,
            'modification_data': register.modified,
            'description': util.process_escape_character(register.abstract),
            'keywords': util.process_escape_character(keywords),
            'catalogo_id': catalogue_id
        }
        register_id = uuid.uuid4()
        df = DataFrame(data=data, columns=columns, index=[register_id])
        data_access.persist_register(df)
        return register_id
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        traceback.print_exc()
        # raise


def find_register_of_catalogue(url_catalogue, catalogue_id):
    '''Busca todos os serviços de cada recuro do catologo e persiste'''
    csw = CatalogueServiceWeb(url=url_catalogue)
    recursosIndisponiveis = []
    verificadoWMS = []
    verificadoWFS = []
    csw.getrecords2()
    i = 20500
    # total = csw.results['matches']
    total = 36000
    alternatives_wms = ('OGC:WMS', 'OGC:WMS-1.1.1-http-get-capabilities')
    while i < total:
        log.info("Indice de records " + str(i))
        csw.getrecords2(maxrecords=100, startposition=i, esn='full')
        for record in csw.records:
            contains_both = False
            log.info("registro: " + record)
            tuple = {}
            for uriDict in csw.records[record].uris:
                if uriDict['protocol'] in alternatives_wms:
                    tuple['wms'] = uriDict['url']
                elif uriDict['protocol'] == 'OGC:WFS':
                    tuple['wfs'] = uriDict['url']
            if tuple.keys().__contains__('wms') and tuple.keys().__contains__('wfs'):
                contains_both = True
            if 'wms' in tuple:
                try:
                    log.info("Encontrado um wms")
                    if not recursosIndisponiveis \
                            .__contains__(tuple['wms']) and not verificadoWMS.__contains__(tuple['wms']):
                        verificadoWMS.append(tuple['wms'])
                        if tuple['wms'] is not None:
                            if contains_both:
                                log.info("ambos serviços disponíveis")
                                persist_wms_service(tuple['wms'], csw.records[record], catalogue_id, tuple['wfs'])
                            else:
                                persist_wms_service(tuple['wms'], csw.records[record], catalogue_id)
                    else:
                        log.info("Já verificado")
                except ConnectTimeout as e:
                    log.info("Falha na requisição: timeout")
                    log.warning("Falha na requisição: timeout")
                    log.info("Serviço: " + str(tuple['wms']))
                    log.warning("Serviço: " + str(tuple['wms']))
                    recursosIndisponiveis.append(tuple['wms'])
                except ReadTimeout as e:
                    log.warning('timeout');
                except Exception as e:
                    log.info("Falha desconhecida durante o processo")
                    log.error(e)
                    log.error(repr(traceback.extract_stack()))
            elif 'wfs' in tuple:
                try:
                    log.info("Encontrado registro um wfs")
                    if not recursosIndisponiveis.__contains__(tuple['wfs']) \
                            and not verificadoWFS.__contains__(tuple['wfs']):
                        verificadoWFS.append(tuple['wfs'])
                        if tuple['wfs'] is not None:
                            persist_wfs_service(tuple['wfs'], csw.records[record], catalogue_id)
                    else:
                        log.info("Já verificado")
                except ConnectTimeout as e:
                    recursosIndisponiveis.append(tuple['wfs'])
                    log.info("Falha na requisição: timeout")
                    log.info("Serviço: " + str(tuple['wfs']))
                except Exception as e:
                    log.error("Falha desconhecida durante o processo")
                    log.error(e)
                    log.error(repr(traceback.extract_stack()))
        i += 100
    log.info('Recursos indisponíveis')
    log.info(recursosIndisponiveis)
    log.info('Recursos verificados WMS')
    log.info(verificadoWMS)
    log.info('Recursos verificados WFS')
    log.info(verificadoWFS)


def build_dataframe_catalogue(url_catalogue):
    ''' Construir Data Frame do catalogo e persistir'''
    try:
        _id = uuid.uuid4()
        df = DataFrame({'url': url_catalogue}, index=[_id])
        data_access.persist_catalogue(df)
        return _id
    except Exception:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


if __name__ == '__main__':
    # http://geoinfo.cnps.embrapa.br/geoserver/geonode/wms
    # http://geoinfo.cpatu.embrapa.br/geoserver/geonode/wfs
    # try:
    catalogue_id = build_dataframe_catalogue('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw')
    find_register_of_catalogue('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw', catalogue_id)
    # except:
    # traceback.print_exc()
