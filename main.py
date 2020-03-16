import traceback
from owslib.csw import CatalogueServiceWeb
from pandas import DataFrame
from requests import ConnectTimeout
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
import util
import data_access
import uuid
import geometry_data

''' Log com as configurações padroes '''
log = util.get_logger()


def persistirFeatureType(content, service_id):
    '''Percorre todos as feições do serviço para armazenar no banco'''
    try:
        data = {
            'title': '',
            'name': '',
            'description': '',
            'keywords': '',
            'service_id': service_id,
            'bounding_box_xmin': '',
            'bounding_box_ymin': '',
            'bounding_box_xmax': '',
            'bounding_box_ymax': ''
        }
        columns = ['title', 'name', 'description', 'keywords', 'service_id',
                   'bounding_box_xmin', 'bounding_box_ymin', 'bounding_box_xmax', 'bounding_box_ymax']
        for featureType in content:
            data['title'] = content[featureType].title
            data['name'] = featureType
            if content[featureType].boundingBox is not None:
                data['bounding_box_xmin'] = content[featureType].boundingBox[0]
                data['bounding_box_ymin'] = content[featureType].boundingBox[1]
                data['bounding_box_xmax'] = content[featureType].boundingBox[2]
                data['bounding_box_ymax'] = content[featureType].boundingBox[3]
            data['description'] = content[featureType].abstract
            if content[featureType].keywords is not None:
                data['keywords'] = ','.join(content[featureType].keywords)
            log.info(data)
            df = DataFrame(data=data, columns=columns, index=[uuid.uuid4()])
            data_access.persist_feature_type(df)
    except:
        raise


def persistirServicoWMS(url_record, record, catalogue_id):
    '''Persiste no banco informações sobre um WMS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wms = WebMapService(url_record)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        register_id = persistirRegistro(record, catalogue_id)
        columns = ['url', 'type', 'title', 'description', 'publisher', 'registro_id',
                   'bounding_box_xmin', 'bounding_box_ymin', 'bounding_box_xmax', 'bounding_box_ymax']
        data = {
            'url': wms.url,
            'type': 'OGC:WMS',
            'title': wms.identification.title,
            'description': wms.identification.abstract,
            'publisher': wms.provider.contact.organization,
            'registro_id': register_id,
            'bounding_box_xmin': '',
            'bounding_box_ymin': '',
            'bounding_box_xmax': '',
            'bounding_box_ymax': ''
        }
        service_id = uuid.uuid4()
        persistirFeatureType(wms.contents, service_id.__str__())
        df = DataFrame(data=data, columns=columns, index=[service_id])
        data_access.persist_service(df)
        return True
    except:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persistirServicoWFS(url_record, record, catalogue_id):
    '''Persiste no banco informações sobre um WFS referente a um catalogo'''
    # TODO falta persistir os features types do WFS tbm
    # TODO lembrar de colocar o service_id.__str__()
    try:
        log.info("Iniciando requisicao")
        wfs = WebFeatureService(url_record)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        register_id = persistirRegistro(record, catalogue_id)
        columns = ['url', 'type', 'title', 'description', 'publisher', 'registro_id',
                   'bounding_box_xmin', 'bounding_box_ymin', 'bounding_box_xmax', 'bounding_box_ymax']
        data = {
            'url': wfs.url,
            'type': 'OGC:WFS',
            'title': wfs.identification.title,
            'description': wfs.identification.abstract,
            'registro_id': register_id,
            'bounding_box_xmin': '',
            'bounding_box_ymin': '',
            'bounding_box_xmax': '',
            'bounding_box_ymax': ''
        }
        '''Verificando se existe os atributos de publisher'''
        if dir(wfs.provider).__contains__('contact') and dir(wfs.provider.contact).__contains__('organization'):
            data['publisher'] = wfs.provider.contact.organization
        else:
            data['publisher'] = None
        df = DataFrame(data=data, columns=columns, index=[uuid.uuid4()])
        data_access.persist_service(df)
    except:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persistirRegistro(register, catalogue_id):
    '''Persisti um novo registro no banco'''
    try:
        log.info('Coleta de dados do registro')
        columns = ['title', 'publisher', 'bounding_box', 'creation_data',
                   'modification_data', 'description', 'keywords', 'catalogo_id']
        if register.bbox is not None:
            bbox = str(
                register.bbox.maxx + ', ' + register.bbox.maxy + ', ' + register.bbox.minx + ', ' + register.bbox.miny)
        else:
            bbox = None
        keywords = None
        if register.subjects is not None:
            words = []
            for subject in register.subjects:
                if subject is not None:
                    words.append(subject)
            keywords = ','.join(words)
        data = {
            'title': register.title,
            'publisher': register.publisher,
            'bounding_box': bbox,
            'creation_data': register.created,
            'modification_data': register.modified,
            'description': register.abstract,
            'keywords': keywords,
            'catalogo_id': catalogue_id
        }
        idRegistro = uuid.uuid4()
        df = DataFrame(data=data, columns=columns, index=[idRegistro])
        data_access.persist_register(df)
        return idRegistro
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        traceback.print_exc()
        # raise


def buscarRegistrosDoCatalogo(url_catalogue, catalogue_id):
    '''Busca todos os serviços de cada recuro do catologo e persiste'''
    csw = CatalogueServiceWeb(url=url_catalogue)
    recursosIndisponiveis = []
    verificadoWMS = []
    verificadoWFS = []
    csw.getrecords2()
    i = 19000
    # total = csw.results['matches']
    total = 19700
    while i < total:
        log.info(f"Indice de records {i}")
        csw.getrecords2(maxrecords=100, startposition=i, esn='full')
        for record in csw.records:
            log.info("registro: " + record)
            tuple = {}
            for uriDict in csw.records[record].uris:
                if uriDict['protocol'] == 'OGC:WMS':
                    tuple['wms'] = uriDict['url']
                elif uriDict['protocol'] == 'OGC:WFS':
                    tuple['wfs'] = uriDict['url']
            if 'wms' in tuple:
                try:
                    log.info("Encontrado um wms")
                    if not recursosIndisponiveis \
                            .__contains__(tuple['wms']) and not verificadoWMS.__contains__(tuple['wms']):
                        verificadoWMS.append(tuple['wms'])
                        persistirServicoWMS(tuple['wms'], csw.records[record], catalogue_id)
                    else:
                        log.info("Já verificado")
                except ConnectTimeout:
                    log.info("Falha na requisição: timeout")
                    log.warning("Falha na requisição: timeout")
                    log.info("Serviço: " + str(tuple['wms']))
                    log.warning("Serviço: " + str(tuple['wms']))
                    recursosIndisponiveis.append(tuple['wms'])
                except Exception as e:
                    log.error(e)
                    log.error(repr(traceback.extract_stack()))
                    log.info("Falha desconhecida durante o processo")
            # if 'wfs' in tuple:
            #     try:
            #         log.info("Encontrado registro um wfs")
            #         if not recursosIndisponiveis.__contains__(tuple['wfs']) \
            #                 and not verificadoWFS.__contains__(tuple['wfs']):
            #             verificadoWFS.append(tuple['wfs'])
            #             persistirServicoWFS(tuple['wfs'], csw.records[record], catalogue_id)
            #         else:
            #             log.info("Já verificado")
            #     except ConnectTimeout:
            #         recursosIndisponiveis.append(tuple['wfs'])
            #         log.info("Falha na requisição: timeout")
            #         log.info("Serviço: " + str(tuple['wfs']))
            #     except Exception as e:
            #         log.error("Falha desconhecida durante o processo")
            #         log.error(e)
            #         log.error(repr(traceback.extract_stack()))

        i += 100
    log.info('Recursos indisponíveis')
    log.info(recursosIndisponiveis)
    log.info('Recursos verificados WMS')
    log.info(verificadoWMS)
    log.info('Recursos verificados WFS')
    log.info(verificadoWFS)


#


def construirDFCatalogo(url_catalogue):
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
    catalogue_id = construirDFCatalogo('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw')
    buscarRegistrosDoCatalogo('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw', catalogue_id)
    geometry_data.start_creation_envelop_services()
    # except:
        # traceback.print_exc()
