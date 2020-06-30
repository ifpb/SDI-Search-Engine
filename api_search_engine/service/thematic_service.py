import pysolr


class ThematicService:
    # TODO É provavel que tenha que tratar a variavel query
    def __init__(self):
        self._solr = pysolr.Solr('http://localhost:8983/solr/inde', always_commit=False, timeout=10)

    def search_in_level_feature_type(self, query, data):
        result = self._solr.search(f'feature_type_metadata:{query}', **{
            'fl': 'feature_type_id, score'
        })
        for r in result:
            if r.keys().__contains__('feature_type_id'):
                data[r['feature_type_id']] = r['score'] / 100

    def search_in_level_service(self, query, data):
        result = self._solr.search(f'service_metadata:{query}', **{
            'fl': 'service_id, score'
        })
        for r in result:
            if r.keys().__contains__('service_id'):
                data[r['service_id']] = r['score'] / 100
