from fibaro.adapter import HomeCenterAdapter
from django.test import TestCase
from django.utils import timezone

# models test
class FibaroAdapterTest(TestCase):

    '''
        Tests that all the info, regarding 
        the Home Center Lite device, that were
        passed through the .evn file are valid.
    '''
    def test_hclite_info(self):
        hca = HomeCenterAdapter()
        self.assertEqual('Pokemon1991', hca.password)
        self.assertEqual('http://192.168.1.19',hca.url)
        self.assertEqual('vasilisalepopoulos@gmail.com', hca.user)
        
    def test_hca_get_pass(self):
        hca = HomeCenterAdapter()
        response = hca.get(method='Get', endpoint='/api/devices')
        self.assertEqual(200, response.status_code)
        
    # This testcase must fail due to an invalid token which is generated
    # from invalid passed data 
    def test_hca_get_fail(self):
        hca = HomeCenterAdapter()
        hca.headers={'Authorization':'thisisnotavalidtoken'}
        response = hca.get(method='Get', endpoint='/api/devices')
        self.assertEqual(401, response.status_code)
    