import requests

from .exceptions import (
    StepikCredentialsError
)

BASE_URL = 'https://stepik.org'
TOKEN_URL = BASE_URL + '/oauth2/token/'
API_URL = BASE_URL + '/api'


class StepikUtil(object):
    def __init__(self, client_id=None, client_secret=None):
        self._token = self._get_token(client_id, client_secret)

    def _get_token(self, client_id, client_secret):
        """
        Получение ключа авторизации для Stepik

        Args:
            client_id (str): Идентификатор приложения
            client_secret (str): Секретный ключ приложения

        Returns:
            token (str): токен авторизации

        Raises:
            StepikCredentialsError: в случае неудачной авторизации
        """
        auth = requests.auth.HTTPBasicAuth(self._client_id, self._client_secret)
        response = requests.post(url=TOKEN_URL,
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth
                                 )
        token = response.json().get('access_token', None)
        if not token:
            raise StepikCredentialsError
        return token
