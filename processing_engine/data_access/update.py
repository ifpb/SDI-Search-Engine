from pyexpat import features

import util
import data_access
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from main import find_date, find_date_in_service_metadata, process_feature_type
import tematic
import geometry_data
from datetime import datetime



''' Log com as configurações padroes '''
log = util.get_logger()
log.info('PROCESSING ENGINE -> DATA ACCESS UPDATE')


def update_feature_type(content, service_description, service_id):
    features = data_access.features_of_service(service_id)
    all_description = ''
    features_solr_docs = []
    solr_docs_remove = []

    for feature in content:
        if features.keys().__contains__(feature):
            log.info('PROCESSING ENGINE -> update_feature_type: update feature type')
            feature_id = features[feature]
            feature_data = {
                'title': util.process_escape_character(content[feature].title),
                'description': util.process_escape_character(content[feature].abstract),
                'keywords': '',
                'start_date': None,
                'end_date': None,
                'features_of_service': len(content),
                'geometry': None,
                'area': None,
                'x_min': content[feature].boundingBox[0],
                'y_min': content[feature].boundingBox[1],
                'x_max': content[feature].boundingBox[2],
                'y_max': content[feature].boundingBox[3],

            }
            #                                      0 = type feature
            feature_data = find_date(feature_data, 0)
            if content[feature].keywords is not None:
                feature_data['keywords'] = util.process_escape_character(
                    ','.join(content[feature].keywords))
            if content[feature].boundingBox is not None:
                feature_data['geometry'] = data_access.create_geometry(
                    content[feature].boundingBox[0],
                    content[feature].boundingBox[1],
                    content[feature].boundingBox[2],
                    content[feature].boundingBox[3])
                feature_data['area'] = data_access.geometry_area(feature_data['geometry'])
            # thematic index
            feature_description = util.build_string_for_solr(
                [feature_data['title'], feature_data['description'], feature_data['keywords']])
            all_description += feature_description
            feature_description += service_description
            try:
                data_access.update_feature_type(feature_data, feature_id)
                features_solr_docs.append(tematic.build_doc_solr_feature_type(feature_description, feature_id))
                solr_docs_remove.append(feature_id)
            except Exception as e:
                log.error('PROCESSING ENGINE -> fail on update_feature_type')
                log.error(f'PROCESSING ENGINE -> {e}')
        else:
            log.info('PROCESSING ENGINE -> update_feature_type: new feature type')
            data = process_feature_type(feature, service_id, content, service_description)
            if data is not None:
                all_description += data['description']
                features_solr_docs.append(data['solr_docs'])
    tematic.remove_documents_feature_type(solr_docs_remove)
    tematic.add_documents_feature_type(features_solr_docs)
    return all_description


def update_service(service, register):
    log.info('PROCESSING ENGINE -> update_service')
    service_data = {
        'id': service[0],
        'wfs_url': service[1],
        'wms_url': service[2],
        'service_processed': service[3]
    }
    if service_data['service_processed'] == 'OGC:WMS':
        service = WebMapService(service_data['wms_url'])
        log.info('PROCESSING ENGINE -> WMS service for update')
    else:
        service = WebFeatureService(service_data['wfs_url'])
        log.info('PROCESSING ENGINE -> WFS service for update')
    if len(service.contents) > 0:
        data = {
            'title': util.process_escape_character(register.title),
            'description': util.process_escape_character(register.abstract),
            'publisher': util.process_escape_character(service.provider.contact.organization),
            'start_date': None,
            'end_date': None,
            'area': None
        }
        if dir(service.provider).__contains__('contact') and dir(service.provider.contact).__contains__('organization'):
            data['publisher'] = util.process_escape_character(service.provider.contact.organization)
        elif register.publisher is not None:
            data['publisher'] = util.process_escape_character(register.publisher)
        else:
            data['publisher'] = None
        data = find_date(data)
        if data['start_date'] and data['end_date'] is None:
            data = find_date_in_service_metadata(data, register.date)
        service_description = util.build_string_for_solr(
            [data['title'], data['description'], data['publisher']]
        )
        service_description += update_feature_type(service.contents, service_description, service_data['id'])
        data_access.update_service_all_data(data, service_data['id'])
        tematic.remove_documents_service([service_data['id']])
        tematic.add_document_service(service_description, service_data['id'])
        geometry_data.create_envelop_of_service(service_data['id'])


def update_register(register, csw_url):
    # TODO update data record
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
        'id': register.identifier + csw_url
    }
    log.info('PROCESSING ENGINE -> Updating register: ' + register.identifier + csw_url)
    data_access.update_register(data)
    # TODO retrieve services associated
    services_associated = data_access.services_of_register(register.identifier + csw_url)
    log.info('PROCESSING ENGINE -> Services associated: ' + str(len(services_associated)))
    # TODO update data of services associated
    for service in services_associated:
        # log.info('PROCESSING ENGINE -> Single Services associated: ' + str(service[3]))
        try:
            update_service(service, register)
        except Exception as e:
            log.error('PROCESSING ENGINE -> fail on update service')
            log.error(f'PROCESSING ENGINE -> {e}')