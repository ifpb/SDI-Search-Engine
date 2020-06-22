import pysolr
import uuid
import util

log = util.get_logger()

solr = pysolr.Solr('http://localhost:8983/solr/inde', always_commit=True, timeout=10)


def add_document_service(data, service_id):
    log.info('Adding a new document service to the solr')
    id = uuid.uuid4().__str__()
    solr.add({
        'id': id,
        'service_metadata': data,
        'service_id': service_id.__str__()
    })


def add_document_feature_type(data, feature_type_id):
    log.info('Adding a new document feature type to the solr')
    id = uuid.uuid4().__str__()
    solr.add({
        'id': id,
        'feature_type_metadata': data,
        'feature_type_id': feature_type_id.__str__()
    })


def add_documents_feature_type(docs):
    log.info(f'Adding {len(docs)} documents feature type to the solr')
    solr.add(docs)


def build_doc_solr_feature_type(data, feature_type_id):
    log.info('Build a new document feature type to the solr')
    id = uuid.uuid4().__str__()
    return {
        'id': id,
        'feature_type_metadata': data,
        'feature_type_id': feature_type_id.__str__()
    }


if __name__ == '__main__':
    print('hello tematic')

    # response = solr.search('feature_type_metadata:*')
    #
    # for r in response:
    #     print(r['feature_type_metadata'])

    if False:
        solr.delete(q='*:*', commit=True)
