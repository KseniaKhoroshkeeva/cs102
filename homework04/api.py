import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    s = requests.Session()
    retry = Retry(max_retries, max_retries, max_retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    try:
        response = requests.get(url, params, timeout=timeout)
        response.raise_for_status()  # выдает исключение при ошибке 500
    except Exception as e:
        print(e)
    else:
        return response


def get_friends(user_id, fields=''):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query = '{domain}/friends.get?user_id={user_id}&fields={fields}&access_token={access_token}&v={version}'.format(
        domain = config.VK_CONFIG['domain'],
        user_id = user_id,
        fields = fields,
        access_token = config.VK_CONFIG['access_token'],
        version = config.VK_CONFIG['version']
    )
    response = requests.get(query)
    return response
