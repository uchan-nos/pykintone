import unittest
import tests.envs as envs
from pykintone.account import Account, kintoneService


class TestAccount(unittest.TestCase):

    def test_auth(self):
        account = Account("test_domain")
        self.assertTrue(account)
        print(account)

    def test_auth_load(self):
        apps = Account.load(envs.FILE_PATH)
        self.assertEqual(1, len(apps))
        print(apps.app())


class TestService(unittest.TestCase):

    def test_value_to_datetime(self):
        from datetime import datetime
        format = lambda d: d.strftime("%Y-%m-%d %H:%M:%S")
        utc = datetime.utcnow().strftime(kintoneService.DATETIME_FORMAT)
        local = format(datetime.now())

        localized = kintoneService.value_to_datetime(utc)
        self.assertEqual(local, format(localized))

    def test_datetime_to_value(self):
        from datetime import datetime
        import pytz
        utc = datetime.utcnow().replace(tzinfo=pytz.UTC).strftime(kintoneService.DATETIME_FORMAT)
        local = datetime.now()

        utced = kintoneService.datetime_to_value(local)
        self.assertEqual(utc, utced)

    def test_app(self):
        kin = Account.loads({
            'domain': 'foo',
            'apps': {
                'app1': {
                    'id': 1,
                    'token': 'dead'
                },
                'app2': {
                    'id': 2,
                    'token': 'beef'
                }
            }
        })
        self.assertIsInstance(kin, kintoneService)

        app1 = kin.app(app_name='app1')
        self.assertEqual(app1.app_name, 'app1')
        self.assertEqual(app1.api_token, 'dead')

        app2 = kin.app(app_name='app2')
        self.assertEqual(app2.app_name, 'app2')
        self.assertEqual(app2.api_token, 'beef')

    def test_app_not_found(self):
        kin = Account.loads({
            'domain': 'foo',
            'apps': {}
        })
        app = kin.app(app_name='app1')
        self.assertIsNone(app)
