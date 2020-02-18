import traceback
from owslib.csw import CatalogueServiceWeb
from pandas import DataFrame
from requests import ConnectTimeout
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
import util
import data_access
import uuid


''' Log com as configurações padroes '''
log = util.getLogger()


def persistirFeatureType(content, idService):
    '''Percorre todos as feições do serviço para armazenar no banco'''
    try:
        data = {
            'title': '',
            'name': '',
            'bounding_box': '',
            'description': '',
            'keywords': '',
            'id_service': idService
        }
        columns = ['title', 'name', 'bounding_box', 'description', 'keywords']
        for featureType in content:
            data['title'] = content[featureType].title
            data['name'] = featureType
            if content[featureType].boundingBox is not None:
                data['bounding_box'] = ','.join([str(e) for e in content[featureType].boundingBox[0:4]])
            data['description'] = content[featureType].abstract
            if content[featureType].keywords is not None:
                data['keywords'] = ','.join(content[featureType].keywords)
            print(data)
            df = DataFrame(data=data, columns=columns, index=[uuid.uuid4()])
            data_access.persistirFeatureType(df)
            df = None
    except:
        raise


def persistirServicoWMS(urlRecord, record, idCatalogo):
    '''Persiste no banco informações sobre um WMS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wms = WebMapService(urlRecord)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        idRegistro = persistirRegistro(record, idCatalogo)
        columns = ['url', 'type', 'title', 'description', 'publisher', 'registro_id']
        data = {
            'url': wms.url,
            'type': 'OGC:WMS',
            'title': wms.identification.title,
            'description': wms.identification.abstract,
            'publisher': wms.provider.contact.organization,
            'registro_id': idRegistro
        }
        idService = uuid.uuid4()
        persistirFeatureType(wms.contents, idService)
        df = DataFrame(data=data, columns=columns, index=[idService])
        data_access.persistirServico(df)
        return True
    except:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persistirServicoWFS(urlRecord, record, idCatalogo):
    '''Persiste no banco informações sobre um WFS referente a um catalogo'''
    try:
        log.info("Iniciando requisicao")
        wfs = WebFeatureService(urlRecord)
        '''Só persisti o registro caso a requisição para o serviço de certo'''
        idRegistro = persistirRegistro(record, idCatalogo)
        columns = ['url', 'type', 'title', 'description', 'publisher', 'registro_id']
        data = {
            'url': wfs.url,
            'type': 'OGC:WFS',
            'title': wfs.identification.title,
            'description': wfs.identification.abstract,
            'registro_id': idRegistro
        }
        '''Verificando se existe os atributos de publisher'''
        if dir(wfs.provider).__contains__('contact') and dir(wfs.provider.contact).__contains__('organization'):
            data['publisher'] = wfs.provider.contact.organization
        else:
            data['publisher'] = None
        df = DataFrame(data=data, columns=columns, index=[uuid.uuid4()])
        data_access.persistirServico(df)
    except:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


def persistirRegistro(registro, idCatalogo):
    '''Persisti um novo registro no banco'''
    try:
        log.info('Coleta de dados do registro')
        columns = ['title', 'publisher', 'bounding_box', 'creation_data',
                   'modification_data', 'description', 'keywords', 'catalogo_id']
        if registro.bbox is not None:
            bbox = str(
                registro.bbox.maxx + ', ' + registro.bbox.maxy + ', ' + registro.bbox.minx + ', ' + registro.bbox.miny)
        else:
            bbox = None
        keywords = None
        if registro.subjects is not None:
            words = []
            for subject in registro.subjects:
                if subject is not None:
                    words.append(subject)
            keywords = ','.join(words)
        data = {
            'title': registro.title,
            'publisher': registro.publisher,
            'bounding_box': bbox,
            'creation_data': registro.created,
            'modification_data': registro.modified,
            'description': registro.abstract,
            'keywords': keywords,
            'catalogo_id': idCatalogo
        }
        idRegistro = uuid.uuid4()
        df = DataFrame(data=data, columns=columns, index=[idRegistro])
        data_access.persistirRegistro(df)
        return idRegistro
    except Exception as e:
        '''Lança a exceção para quem chamou esse escopo'''
        traceback.print_exc()
        # raise


def buscarRegistrosDoCatalogo(cataglogoURL, idCatalogo):
    '''Busca todos os serviços de cada recuro do catologo e persiste'''
    csw = CatalogueServiceWeb(url=cataglogoURL)
    recursosIndisponiveis = []
    verificadoWMS = []
    verificadoWFS = []
    csw.getrecords2()
    i = 0
    total = csw.results['matches']
    # total = 5000
    while i < total:
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
                        persistirServicoWMS(tuple['wms'], csw.records[record], idCatalogo)
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
            if 'wfs' in tuple:
                try:
                    log.info("Encontrado registro um wfs")
                    if not recursosIndisponiveis.__contains__(tuple['wfs']) \
                            and not verificadoWFS.__contains__(tuple['wfs']):
                        verificadoWFS.append(tuple['wfs'])
                        persistirServicoWFS(tuple['wfs'], csw.records[record], idCatalogo)
                    else:
                        log.info("Já verificado")
                except ConnectTimeout:
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


#


def construirDFCatalogo(urlCatalogo):
    ''' Construir Data Frame do catalogo e persistir'''
    try:
        idCatalogo = uuid.uuid4()
        df = DataFrame({'url': urlCatalogo}, index=[idCatalogo])
        data_access.persistirCatalogo(df)
        return idCatalogo
    except Exception:
        '''Lança a exceção para quem chamou esse escopo'''
        raise


if __name__ == '__main__':
    # http://geoinfo.cnps.embrapa.br/geoserver/geonode/wms
    # http://geoinfo.cpatu.embrapa.br/geoserver/geonode/wfs
    # try:
    idCatalogo = construirDFCatalogo('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw')
    buscarRegistrosDoCatalogo('http://www.metadados.inde.gov.br/geonetwork/srv/por/csw', idCatalogo)
# except:
# traceback.print_exc()
