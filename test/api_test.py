# import unittest
# from app import app
#

import unittest
from app import app
class AddEndpointTest(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()
    def test_add_success(self):
        payload = {
            'a': 10,
            'b': 5
        }
        response = self.client.post('/math/add', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'result': 15})
    def test_add_missing_param(self):
        payload = {
            'a': 10  # Missing 'b'
        }
        response = self.client.post('/math/add', json=payload)
        self.assertEqual(response.status_code, 400)
if __name__ == '__main__':
    unittest.main()


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()
