import os
from unittest import skip  # noqa
from alephclient.tasks.util import load_config_file

from aleph.logic.entities import bulk_load
from aleph.model import Collection
from aleph.tests.util import TestCase


class BulkLoadTestCase(TestCase):

    def setUp(self):
        super(BulkLoadTestCase, self).setUp()

    def test_load_sqlite(self):
        count = Collection.all().count()
        assert 0 == count, count

        db_uri = 'sqlite:///' + self.get_fixture_path('kek.sqlite')
        os.environ['ALEPH_TEST_BULK_DATABASE_URI'] = db_uri
        yml_path = self.get_fixture_path('kek.yml')
        config = load_config_file(yml_path)
        bulk_load(config)

        count = Collection.all().count()
        assert 1 == count, count

        coll = Collection.by_foreign_id('kek')
        assert coll.category == 'scrape', coll.category

        _, headers = self.login(is_admin=True)
        self.flush_index()

        res = self.client.get('/api/2/entities?q=friede+springer',
                              headers=headers)
        assert res.status_code == 200, res
        assert res.json['total'] == 1, res.json
        res0 = res.json['results'][0]
        assert res0['id'] == '9895ccc1b3d6444ccc6371ae239a7d55c748a714', res0

    def test_load_csv(self):
        count = Collection.all().count()
        assert 0 == count, count

        db_uri = 'file://' + self.get_fixture_path('experts.csv')
        os.environ['ALEPH_TEST_BULK_CSV'] = db_uri
        yml_path = self.get_fixture_path('experts.yml')
        config = load_config_file(yml_path)
        bulk_load(config)

        coll = Collection.by_foreign_id('experts')
        assert coll.category == 'scrape', coll.category

        _, headers = self.login(is_admin=True)
        self.flush_index()

        count = Collection.all().count()
        assert 1 == count, count

        res = self.client.get('/api/2/entities?q=Greenfield',
                              headers=headers)
        assert res.status_code == 200, res
        assert res.json['total'] == 1, res.json
        res0 = res.json['results'][0]
        assert res0['id'] == '6897ef1acd633c229d812c1c495f030d212c9081', res0
