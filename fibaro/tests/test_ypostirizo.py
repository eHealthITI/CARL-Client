from fibaro.ypostirizo import Cloud
from fibaro.adapter import HomeCenterAdapter
from django.test import TestCase
from django.utils import timezone

# models test
class CloudTest(TestCase):
    '''
        Tests that all the info, regarding 
        the Home Center Lite device, that were
        passed through the .evn file are valid.
    '''
    def test_cloud_info(self):
        cloud = Cloud()
        self.assertEqual('http://127.0.0.1:83', cloud.url)
        self.assertEqual('1b113efc8f44c1285e106ce623dfb7fbfa5b4926',cloud.token)
        self.assertDictEqual({'authorization' : 'Token 1b113efc8f44c1285e106ce623dfb7fbfa5b4926'}, cloud.headers)
        
    # def test_get_pass(self):
    #     cloud = Cloud()
    #     cloud.url='https://cloud.ypostirizo.iti.gr'
    #     response = cloud.send(endpoint='/api/device/v2/sleep/day/sum/2020-10-05/2020-12-10')
    #     self.assertEqual(200, response.status_code)