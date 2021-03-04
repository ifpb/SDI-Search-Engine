import traceback
from owslib.csw import CatalogueServiceWeb
from pandas import DataFrame
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from requests import ConnectTimeout, ReadTimeout, HTTPError
from datetime import datetime

# from

import tematic
import util
import data_access
from data_access import update as data_access_update
import uuid
import geometry_data
import datetime
import schedule
import time

# turn off future warnings
import warnings

import tagging_temporal
from exception import NoFeaturesOfService

warnings.simplefilter(action='ignore', category=FutureWarning)

''' Log com as configurações padroes '''
log = util.get_logger()

TYPE_FEATURE_TYPE = 0
TYPE_SERVICE = 1


def find_date(data, type=TYPE_SERVICE):
    # search for dates in text
    if data['title'] is not None:
        result = tagging_temporal.find_date(data['title'])
        if result is None:
            if data['description'] is not None:
                result = tagging_temporal.find_date(data['description'])
                if result is not None:
                    log.info('PROCESSING ENGINE -> TAGGING - date in description')
                    data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
                    data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
                else:
                    if type != TYPE_SERVICE:
                        if data['keywords'] is not None:
                            result = tagging_temporal.find_date(data['keywords'])
                            if result is not None:
                                log.info('PROCESSING ENGINE -> TAGGING - date in keywords')
                                data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
                                data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
                            else:
                                log.info('PROCESSING ENGINE -> TAGGING - feature type without date')
        else:
            log.info('PROCESSING ENGINE -> TAGGING - date in title')
            data['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
            data['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
    return data


def find_date_in_service_metadata(service_date, date_attribute):
    result = tagging_temporal.find_date(date_attribute)
    if result is not None:
        service_date['start_date'] = datetime.datetime.strptime(result['start_date'], '%d/%m/%Y').date()
        service_date['end_date'] = datetime.datetime.strptime(result['end_date'], '%d/%m/%Y').date()
    return service_date


def process_feature_type(featureType, service_id, content, service_description):
    data = {'title': '', 'name': '', 'description': '', 'keywords': '', 'service_id': service_id,
            'start_date': None, 'end_date': None, 'geometry': '', 'area': None, 'features_of_service': len(content),
            'x_min': None, 'y_min': None, 'x_max': None, 'y_max': None}
    columns = [
        'title', 'name', 'description', 'keywords', 'service_id', 'geometry',
        'start_date', 'end_date', 'area', 'features_of_service', 'x_min', 'y_min',
        'x_max', 'y_max'
    ]
    # bbox
    description_all_features = ''
    data['x_min'] = content[featureType].boundingBox[0]
    data['y_min'] = content[featureType].boundingBox[1]
    data['x_max'] = content[featureType].boundingBox[2]
    data['y_max'] = content[featureType].boundingBox[3]
    feature_type_id = uuid.uuid4()
    data['title'] = util.process_escape_character(content[featureType].title)
    data['name'] = util.process_escape_character(featureType)
    if content[featureType].keywords is not None:
        data['keywords'] = util.process_escape_character(
            ','.join(content[featureType].keywords))
    data['description'] = util.process_escape_character(content[featureType].abstract)
    data = find_date(data, TYPE_FEATURE_TYPE)
    if not data_access.exists_feature_type(data):
        # thematic index
        feature_description = util.build_string_for_solr([data['title'], data['description'], data['keywords']])
        description_all_features += feature_description
        feature_description += service_description
        if content[featureType].boundingBox is not None:
            data['geometry'] = data_access.create_geometry(
                content[featureType].boundingBox[0],
                content[featureType].boundingBox[1],
                content[featureType].boundingBox[2],
                content[featureType].boundingBox[3])
            data['area'] = data_access.geometry_area(data['geometry'])
        log.info('PROCESSING ENGINE -> Feature Type: ' + data['title'])
        df = DataFrame(data=data, columns=columns, index=[feature_type_id])
        data_access.persist_feature_type(df)
        return {
            'description': description_all_features,
            'solr_doc': tematic.build_doc_solr_feature_type(feature_description, feature_type_id)
        }
    else:
        log.info('PROCESSING ENGINE -> exists feature-> name: ' + data['name'])
        return None


def persist_feature_type(content, service_description, service_id):
    '''Percorre todos as feições do serviço para armazenar no banco'''
    try:
        features_solr_docs = []
        all_description = ''
        log.info("PROCESSING ENGINE -> total features: " + str(len(content)))
        for featureType in content:
            data = process_feature_type(featureType, service_id, content, service_description)
            if data is not None:
                features_solr_docs.append(data['solr_doc'])
                all_description += data['description']
        if features_solr_docs.__len__() == 0:
            raise NoFeaturesOfService.NoFeaturesOfService()
        tematic.add_documents_feature_type(features_solr_docs)
        return all_description
    except Exception as e:
        raise e


def persist_wms_service(url_record, record, catalogue_id, url_wfs=None):
    '''Persiste no banco informações sobre um WMS referente a um catalogo'''
    try:
        log.info("PROCESSING ENGINE -> Starting request")
        wms = WebMapService(url_record)
        if len(wms.contents) > 0:
            columns = [
                'wfs_url', 'wms_url', 'service_processed', 'title',
                'description', 'publisher', 'register_id', 'geometry',
                'start_date', 'end_date', 'area', 'x_min', 'y_min', 'x_max', 'y_max'
            ]
            data = {
                'wms_url': wms.url,
                'service_processed': 'OGC:WMS',
                'title': util.process_escape_character(record.title),
                'description': util.process_escape_character(record.abstract),
                'register_id': '',
                'start_date': None,
                'end_date': None,
                'area': None
            }
            service_id = uuid.uuid4()
            if dir(wms.provider).__contains__('contact') and dir(wms.provider.contact).__contains__('organization'):
                data['publisher'] = util.process_escape_character(
                    wms.provider.contact.organization)
            elif record.publisher is not None:
                data['publisher'] = util.process_escape_character(record.publisher)
            else:
                data['publisher'] = None
            service_description = util.build_string_for_solr(
                [data['title'], data['description'], data['publisher']]
            )
            service_description += persist_feature_type(wms.contents, service_description, service_id.__str__())
            '''Só persisti o registro caso a requisição para o serviço de certo'''
            register_id = persist_register(record, catalogue_id)
            data['register_id'] = register_id

            if url_wfs is not None:
                data['wfs_url'] = url_wfs

            data = find_date(data)
            if data['start_date'] and data['end_date'] is None:
                data = find_date_in_service_metadata(data, record.date)
            # thematic index
            tematic.add_document_service(service_description, service_id)

            df = DataFrame(data=data, columns=columns, index=[service_id])
            data_access.persist_service(df)
            geometry_data.create_envelop_of_service(service_id)
        else:
            log.info('PROCESSING ENGINE -> service without feature types')
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persist_wfs_service(url_record, record, catalogue_id):
    '''Persiste no banco informações sobre um WFS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wfs = WebFeatureService(url_record)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        if len(wfs.contents) > 0:
            service_id = uuid.uuid4()

            columns = [
                'wfs_url', 'wms_url', 'service_processed', 'title',
                'description', 'publisher', 'register_id', 'geometry',
                'start_date', 'end_date', 'area', 'x_min', 'y_min', 'x_max', 'y_max'
            ]
            data = {
                'wfs_url': wfs.url,
                'service_processed': 'OGC:WFS',
                'title': util.process_escape_character(record.title),
                'description': util.process_escape_character(record.abstract),
                'register_id': '',
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

            service_description = util.build_string_for_solr(
                [data['title'], data['description'], data['publisher']]
            )
            service_description += persist_feature_type(wfs.contents, service_description, service_id.__str__())

            register_id = persist_register(record, catalogue_id)
            data['register_id'] = register_id

            data = find_date(data)
            if data['start_date'] and data['end_date'] is None:
                data = find_date_in_service_metadata(data, record.date)
            # thematic index

            tematic.add_document_service(service_description, service_id)

            df = DataFrame(data=data, columns=columns, index=[service_id])
            data_access.persist_service(df)
            geometry_data.create_envelop_of_service(service_id)
        else:
            log.info('PROCESSING ENGINE -> service without feature types')
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persist_register(register, catalogue_id):
    '''Persisti um novo registro no banco'''
    try:
        log.info('PROCESSING ENGINE -> Coleta de dados do registro')
        columns = ['title', 'publisher', 'date', 'description', 'keywords', 'catalogue_id']
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
            'date': register.date.replace('/', '-'),
            'description': util.process_escape_character(register.abstract),
            'keywords': util.process_escape_character(keywords),
            'catalogue_id': catalogue_id
        }
        register_id = register.identifier + current_csw_url
        df = DataFrame(data=data, columns=columns, index=[register_id])
        data_access.persist_register(df)
        return register_id
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        traceback.print_exc()
        # raise


def update_registers(registers):
    # TODO remover os registers processados para caso de error não perder o processamento do resto da lista
    log.info(f'PROCESSING ENGINE -> {str(len(registers))} records for update')
    for register in registers:
        try:
            data_access_update.update_register(register, current_csw_url)
        except Exception as e:
            log.error('PROCESSING ENGINE -> fail on update record/service/feature')
            log.error(e)


def add_records(records, catalogue_id, from_update=False):
    log.info(f'PROCESSING ENGINE -> {str(len(records))} possible records for add')
    recursosIndisponiveis = []
    verificadoWMS = []
    verificadoWFS = []
    contains_both = False
    # alternatives_wms = ('OGC:WMS', 'OGC:WMS-1.1.1-http-get-capabilities')
    for record in records:
        if from_update:
            identifier = record.identifier
            record_data = record
        else:
            identifier = records[record].identifier
            record_data = records[record]
        if identifier is not None:
            log.info("PROCESSING ENGINE -> record: " + record_data.identifier)
            tuple = {}
            log.info("PROCESSING ENGINE -> Analyzing URIs")
            for uriDict in record_data.uris:
                if uriDict['protocol'] == 'OGC:WMS':
                    tuple['wms'] = uriDict['url']
                elif uriDict['protocol'] == 'OGC:WFS':
                    tuple['wfs'] = uriDict['url']
            if len(tuple) == 0:
                log.info("PROCESSING ENGINE -> Analyzing references")
                for ref in record_data.references:
                    if ref['scheme'] == 'OGC:WMS':
                        tuple['wms'] = ref['url']
                    elif ref['scheme'] == 'OGC:WFS':
                        tuple['wfs'] = ref['url']
            if tuple.keys().__contains__('wms') and tuple.keys().__contains__('wfs'):
                contains_both = True
            if 'wms' in tuple:
                try:
                    log.info("PROCESSING ENGINE -> found a record wms: " + tuple['wms'])
                    if not recursosIndisponiveis.__contains__(tuple['wms']) and not verificadoWMS.__contains__(tuple['wms']):
                        verificadoWMS.append(tuple['wms'])
                        if tuple['wms'] is not None:
                            if contains_both:
                                if tuple.keys().__contains__('wfs') and tuple['wfs'] is not None:
                                    log.info("PROCESSING ENGINE -> both services available")
                                    persist_wms_service(tuple['wms'], record_data, catalogue_id, tuple['wfs'])
                                else:
                                    persist_wms_service(tuple['wms'], record_data, catalogue_id)
                            else:
                                persist_wms_service(tuple['wms'], record_data, catalogue_id)
                    else:
                        log.info("PROCESSING ENGINE -> has been verified")
                except HTTPError as e:
                    log.warning("Request fail: HTTPError")
                    log.warning(e)
                except ConnectTimeout as e:
                    log.warning("Request fail: timeout")
                    log.warning("Service: " + str(tuple['wms']))
                    recursosIndisponiveis.append(tuple['wms'])
                except ReadTimeout as e:
                    log.warning('PROCESSING ENGINE -> Timeout')
                except NoFeaturesOfService.NoFeaturesOfService as e:
                    log.warning("PROCESSING ENGINE -> NoFeaturesOfService")
                    log.warning("PROCESSING ENGINE -> All the content of this service has already been processed from another")
                except Exception as e:
                    log.info("PROCESSING ENGINE -> Unknown error during the process")
                    log.error(e)
                    # log.error(repr(traceback.extract_stack()))
            elif 'wfs' in tuple:
                try:
                    log.info("PROCESSING ENGINE -> found a record wfs: " + tuple['wfs'])
                    if not recursosIndisponiveis.__contains__(tuple['wfs']) and not verificadoWFS.__contains__(tuple['wfs']):
                        verificadoWFS.append(tuple['wfs'])
                        if tuple['wfs'] is not None:
                            persist_wfs_service(tuple['wfs'], record_data, catalogue_id)
                    else:
                        log.info("PROCESSING ENGINE -> has been verified")
                except HTTPError as e:
                    log.warning("Request fail: HTTPError - " + e)
                except ConnectTimeout as e:
                    log.warning("Request fail: timeout")
                    log.warning("Service: " + str(tuple['wfs']))
                    recursosIndisponiveis.append(tuple['wfs'])
                except ReadTimeout as e:
                    log.warning('PROCESSING ENGINE -> Timeout')
                except NoFeaturesOfService.NoFeaturesOfService as e:
                    log.warning("PROCESSING ENGINE -> NoFeaturesOfService")
                    log.warning("PROCESSING ENGINE -> All the content of this service has already been processed from another")
                except Exception as e:
                    log.info("PROCESSING ENGINE -> Unknown error during the process")
                    log.error(e)
                    # log.error(repr(traceback.extract_stack()))
    log.info('PROCESSING ENGINE -> Recursos indisponíveis')
    log.info(recursosIndisponiveis)
    log.info('PROCESSING ENGINE -> Recursos verificados WMS')
    log.info(verificadoWMS)
    log.info('PROCESSING ENGINE -> Recursos verificados WFS')
    log.info(verificadoWFS)


def find_register_of_catalogue(url_catalogue, catalogue_id, update_records_flag=False):
    '''Busca todos os serviços de cada recuro do catologo e persiste'''
    try:
        csw = CatalogueServiceWeb(url=url_catalogue)
        csw.getrecords2()
        i = 18600
        total = csw.results['matches']
        # total = 1000
        log.info('PROCESSING ENGINE -> Total Records: ' + str(total))
        if update_records_flag:
            records_of_catalogue = data_access.registers_of_catalogue(catalogue_id)
            if len(records_of_catalogue) == 0:
                update_records_flag = False
        if update_records_flag:
            while i < total:
                records_for_add = []
                records_for_update = []
                log.info("PROCESSING ENGINE -> Record Index " + str(i))
                csw.getrecords2(maxrecords=100, startposition=i, esn='full')
                for record_name in csw.records:
                    if csw.records[record_name].identifier is not None:
                        record = csw.records[record_name]
                        if record.identifier + current_csw_url in records_of_catalogue.keys():
                            try:
                                current_date = records_of_catalogue[record.identifier + current_csw_url]
                                updated_date = datetime.datetime.strptime(record.date.replace('/', '-'), '%Y-%m-%d').date()
                                if updated_date > current_date:
                                    log.info(
                                        "PROCESSING ENGINE -> update record: " + record.identifier + current_csw_url)
                                    records_for_update.append(record)
                                else:
                                    log.info("PROCESSING ENGINE -> Record is last: " + record.identifier + current_csw_url)
                            except Exception as e:
                                log.warning('PROCESSING ENGINE -> Fail on load date:')
                                log.warning('PROCESSING ENGINE -> date format: ' + str(
                                    records_of_catalogue[record.identifier + current_csw_url]))
                                log.warning('PROCESSING ENGINE -> date format: ' + str(record.date.replace('/', '-')))
                                log.error(e)
                        else:
                            log.info("PROCESSING ENGINE -> Update Record: New: " + record.identifier + current_csw_url)
                            records_for_add.append(record)
                update_registers(records_for_update)
                add_records(records_for_add, catalogue_id, True)
                i += 100
        else:
            while i < total:
                log.info("PROCESSING ENGINE -> Indice de records " + str(i))
                csw.getrecords2(maxrecords=100, startposition=i, esn='full')
                add_records(csw.records, catalogue_id)
                i += 100
    except Exception as e:
        raise


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


#


def update_or_add_catalogue(catalogue_url):
    catalogue = data_access.retrieve_catalogue_by_url(catalogue_url)
    if catalogue is not None:
        log.info('PROCESSING ENGINE -> UPDATE CATALOGUE: ' + catalogue_url)
        find_register_of_catalogue(catalogue_url, catalogue[0], update_records_flag=True)
    else:
        log.info('PROCESSING ENGINE -> ADD NEW CATALOGUE: ' + catalogue_url)
        catalogue_id = build_dataframe_catalogue(catalogue_url)
        find_register_of_catalogue(catalogue_url, catalogue_id)


current_csw_url = ''


def run():
    try:
        catalogues = [
            'http://www.metadados.inde.gov.br/geonetwork/srv/por/csw',
            # 'https://www.sciencebase.gov/catalog/csw',
            # 'http://bdgex.eb.mil.br/csw'
            # 'http://geoinfo.cnpm.embrapa.br/catalogue/csw'
        ]
        for c in catalogues:
            current_csw_url = c
            update_or_add_catalogue(c)
            # catalogue_id = build_dataframe_catalogue(c)
            # find_register_of_catalogue(c, catalogue_id)
    except:
        log.error(' -- PROCESSING ENGINE - ERROR -- ')
        traceback.print_exc()


schedule.every().day.at("00:00").do(run)

if __name__ == '__main__':
    log.info(' -- PROCESSING ENGINE -- ')
    while True:
        schedule.run_pending()
        print(time.ctime())
        time.sleep(1)
    # or
    # log.info(' -- Sleep 15s -- ')
    # time.sleep(15)
    # run()
