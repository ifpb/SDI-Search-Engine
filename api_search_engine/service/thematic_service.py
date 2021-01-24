import pysolr


class ThematicService:
    # TODO É provavel que tenha que tratar a variavel query
    def __init__(self):
        # container
        self._solr = pysolr.Solr(
            'http://solr_app:8983/solr/inde', always_commit=False, timeout=10)
        # local
        # self._solr = pysolr.Solr(
        #     'http://localhost:8983/solr/inde', always_commit=False, timeout=10)

    def search_in_level_feature_type(self, query, data):
        result = self._solr.search(f'feature_type_metadata:{query}', **{
            'fl': 'id, score',
            'rows': 999999
        })
        for r in result:
            if r.keys().__contains__('id'):
                data[r['id']] = r['score'] / 100

    def search_in_level_service(self, query, data):
        result = self._solr.search(f'service_metadata:{query}', **{
            'fl': 'id, score',
            'rows': 999999
        })
        for r in result:
            if r.keys().__contains__('id'):
                data[r['id']] = r['score'] / 100
