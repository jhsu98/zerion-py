import time
import re
import jwt
import requests
import json
from pprint import pprint
from abc import abstractmethod, ABC

import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Response:
    def __init__(self, r):
        self.headers = r.headers
        self.status_code = r.status_code
        self.response = r.json()

    def __repr__(self):
        return str(self.status_code)

    def __str__(self):
        return str(self.status_code)

class API(ABC):
    def __init__(self, server=None, client_key=None, client_secret=None, params={}):
        if not isinstance(server, str) or not isinstance(client_key, str) or not isinstance(client_secret, str):
            raise TypeError("Invalid API credentials")

        self.__server = server
        self.__client_key = client_key
        self.__client_secret = client_secret
        self.__params = params
        self.__access_token = None
        self.__access_token_expiration = None
        self.__start_time = None
        self.__session = requests.Session()
        self.__session.headers.update({'Content-Type': 'application/json'})
        self.__api_calls = 0
        self.__last_execution_time = None
        self.__rate_limit_retry = params.get('rate_limit_retry', False)
        self.__ifb_api_credentials = params.get('ifb_api_credentials', False)
        self.__region = params.get('region', 'us')
        self.__version = params.get('version', 8.0)

        self.requestAccessToken()
        
    def requestAccessToken(self):
        """Create JWT and request iFormBuilder Access Token
        If token is successfully returned, stored in session header
        Else null token is stored in session header
        """
        try:
            if self.__ifb_api_credentials:
                url = f"https://{self.__region+'-api' if self.__region != 'us' else 'api'}.iformbuilder.com/exzact/api/v{str(self.__version).replace('.','')}/{self.__server}/oauth/token"
                # url = f"https://{self.__server}.iformbuilder.com/exzact/api/oauth/token"
            else:
                url = "https://identity.zerionsoftware.com/oauth2/token"
            # url = "https://qa-identity.zerionsoftware.com/oauth2/token" if self.__isQA else "https://identity.zerionsoftware.com/oauth2/token"

            jwt_payload = {
                'iss': self.__client_key,
                'aud': url,
                'iat': time.time(),
                'exp': time.time() + 300
            }

            encoded_jwt = jwt.encode(
                jwt_payload, self.__client_secret, algorithm='HS256')
            token_body = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': encoded_jwt
            }

            result = requests.post(url, data=token_body, timeout=5)
            result.raise_for_status()
        except Exception as e:
            print(f'Exception: {e}')
            return
        else:
            self.__start_time = time.time()
            self.__access_token = result.json()['access_token']
            self.__session.headers.update(
                {'Authorization': "Bearer %s" % self.__access_token})
            self.__access_token_expiration = time.time() + 3300

    def getParams(self):
        return self.__params

    def getAccessToken(self):
        return self.__access_token

    def getAccessTokenExpiration(self):
        return self.__access_token_expiration

    def getApiCount(self):
        return self.__api_calls

    def getLastExecution(self):
        return self.__last_execution_time

    def getStartTime(self):
        return self.__start_time

    def getApiLifetime(self):
        return round(time.time() - self.__start_time, 2)

    def call(self, method, resource, body=None):
        if self.getAccessToken() is not None and time.time() > self.getAccessTokenExpiration():
            self.requestAccessToken()

        method = method.upper()
        
        if method not in ('GET','POST','PUT','DELETE'):
            raise ValueError(f'{method} is not an accepted method')

        isRateLimited = False

        while not isRateLimited:
            if method == 'GET':
                result = self.__session.get(resource)
            elif method == 'POST':
                result = self.__session.post(resource, data=json.dumps(body))
            elif method == 'PUT':
                result = self.__session.put(resource, data=json.dumps(body))
            elif method == 'DELETE':
                result = self.__session.delete(resource)

            self.__api_calls += 1
            self.__last_execution_time = result.elapsed

            if result.status_code == 429 and self.__rate_limit_retry == True:
                print(f'Rate Limited for {resource}, waiting 60 seconds to retry...')
                time.sleep(60)
            else:
                isRateLimited = True

        return Response(result)

    @abstractmethod
    def describeResources(self):
        raise NotImplementedError

    @abstractmethod
    def describeResource(self, resource):
        raise NotImplementedError