import requests


class ApiClient:
    Base_URL = 'https://restful-booker.herokuapp.com/'

    def get(self, endpoint, params=None):
        return requests.get(f'{self.Base_URL}/{endpoint}', params=params)

    def post(self, endpoint, json=None, headers=None):
        return requests.post(f'{self.Base_URL}/{endpoint}', json=json, headers=headers)

    def put(self, endpoint, params=None, json=None, headers=None):
        return requests.put(f'{self.Base_URL}/{endpoint}', params=params, json=json, headers=headers)

    def patch(self, endpoint, params=None, json=None, headers=None):
        return requests.patch(f'{self.Base_URL}/{endpoint}', params=params, json=json, headers=headers)

    def delete(self, endpoint, params=None, headers=None):
        return requests.delete(f'{self.Base_URL}/{endpoint}', headers=headers)


