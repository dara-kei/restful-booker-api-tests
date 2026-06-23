import requests
from utils.logger_config import logger

class ApiClient:
    BASE_URL = 'https://restful-booker.herokuapp.com'

    def get(self, endpoint, params=None):
        logger.info(f"GET {self.BASE_URL}/{endpoint}")
        logger.debug(f"params: {params}")
        response = requests.get(f'{self.BASE_URL}/{endpoint}', params=params)
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response


    def post(self, endpoint, json=None, headers=None):
        logger.info(f"POST {self.BASE_URL}/{endpoint}")
        logger.debug(f"json: {json}")
        logger.debug(f"headers: {headers}")
        response = requests.post(f'{self.BASE_URL}/{endpoint}', json=json, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response

    def put(self, endpoint, params=None, json=None, headers=None):
        logger.info(f"PUT {self.BASE_URL}/{endpoint}")
        logger.debug(f"params: {params}")
        logger.debug(f"json: {json}")
        logger.debug(f"headers: {headers}")
        response = requests.put(f'{self.BASE_URL}/{endpoint}', params=params, json=json, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response

    def patch(self, endpoint, params=None, json=None, headers=None):
        logger.info(f"PATCH {self.BASE_URL}/{endpoint}")
        logger.debug(f"params: {params}")
        logger.debug(f"json: {json}")
        logger.debug(f"headers: {headers}")
        response = requests.patch(f'{self.BASE_URL}/{endpoint}', params=params, json=json, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response

    def delete(self, endpoint, params=None, headers=None):
        logger.info(f"DELETE {self.BASE_URL}/{endpoint}")
        logger.debug(f"params: {params}")
        logger.debug(f"headers: {headers}")
        response = requests.delete(f'{self.BASE_URL}/{endpoint}', params=params, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response


