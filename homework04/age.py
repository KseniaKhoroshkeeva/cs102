import datetime as dt
#from statistics import median
from typing import Optional

from api import get_friends
#from api_models import User

def median(arr: list):
    arr.sort()
    if len(arr) % 2:
        # для нечетного кол-ва
        return float(arr[len(arr) // 2])
    else:
        # для четного кол-ва
        return (float(arr[len(arr) // 2 - 1]) + float(arr[len(arr) // 2])) / 2

def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    ages = []
    resp = get_friends(user_id, 'bdate')
    for u in resp.json()['response']['items']:
        try:
            bdate = dt.datetime.strptime(u['bdate'], '%d.%m.%Y')
            today = dt.datetime.today()
            age = today.year - bdate.year
            if (bdate.month > today.month) or (bdate.month == today.month and bdate.day > today.day):
                age -= 1
            ages.append(age)
        except:
            pass
    if len(ages):
        return median(ages)
    else:
        return None