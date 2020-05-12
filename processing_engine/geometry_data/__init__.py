import data_access
import util

''' Log com as configurações padroes '''
log = util.get_logger()

if __name__ == '__main__':
    print('inicia a preparação para criação dos envelop')


def start_creation_envelop_services():
    """ Cria os envelop de cada serviço armazenado """
    log.info('start geometry_data')
    services_id = data_access.find_all_services_id()
    for service in services_id:
        log.info(f"criando bbox do servico {service}")
        bbox_of_service = data_access.create_bounding_box_of_service(service)
        log.info(f"atualizando service: {service}")
        data_access.update_service(service, bbox_of_service)
    log.info('end geometry_data')


def create_envelop_of_service(service_id):
    """ Cria o envelope do serviço passado """
    log.info(f"started creation bbox of service {service_id}")
    bbox_of_service = data_access.create_bounding_box_of_service(service_id)
    log.info(f"atualizando service: {service_id}")
    data_access.update_service(service_id, bbox_of_service)
