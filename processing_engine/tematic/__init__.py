import pysolr
import uuid
import util

log = util.get_logger()

solr = pysolr.Solr('http://localhost:8983/solr/inde', always_commit=True, timeout=10)


def add_document_service(data, service_id):
    log.info('SOLR -> Adding a new document service to the solr')
    # id = uuid.uuid4().__str__()
    solr.add({
        'id': service_id.__str__(),
        'service_metadata': data,
    })


def add_document_feature_type(data, feature_type_id):
    log.info('SOLR -> Adding a new document feature type to the solr')
    # id = uuid.uuid4().__str__()
    solr.add({
        'id': feature_type_id.__str__(),
        'feature_type_metadata': data,
    })


def add_documents_feature_type(docs):
    log.info(f'SOLR -> Adding {len(docs)} documents feature type to the solr')
    solr.add(docs)


def build_doc_solr_feature_type(data, feature_type_id):
    log.info('SOLR -> Build a new document feature type to the solr')
    # id = uuid.uuid4().__str__()
    return {
        'id': feature_type_id.__str__(),
        'feature_type_metadata': data,
    }


def remove_documents_feature_type(docs_id):
    log.info(f'SOLR -> Remove {len(docs_id)} feature types documents to the solr')
    solr.delete(id=docs_id)


def remove_documents_service(docs_id):
    log.info(f'SOLR -> Remove {len(docs_id)} services documents to the solr')
    solr.delete(id=docs_id)


if __name__ == '__main__':
    print('hello tematic')

    # response = solr.search('feature_type_metadata:*')
    #
    # for r in response:
    #     print(r['feature_type_metadata'])
    # remove_document_feature_type('eabcf6c8-7326-4175-b570-e2399fb490a9')
    solr.delete(feature_type_id='d998c100-f88a-4a7c-a86f-e415e102f195')
    if False:
        solr.delete(q='*:*', commit=True)
