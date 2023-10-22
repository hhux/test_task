import datetime

import pytest
import requests


class TestApiUsers:
    base_url = 'https://reqres.in/api/users'

    def test_get_all_users_hp(self):
        """Получение информации о всех пользователях"""
        expected_fields = ['id', 'email', 'first_name', 'last_name', 'avatar']
        response = requests.get(self.base_url)
        assert response.status_code == 200
        for field in expected_fields:
            assert field in response.json()['data'][0], f"Поле {field} отсутствует в ответе"
            assert response.json()['data'][0][field], f"Поле {field} пустое в ответе"

    def test_get_specific_user(self):
        """Получение информации о конкретном пользователе"""
        user_id = 6
        url = f'{self.base_url}/{user_id}'
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()['data']['id'] == user_id, f"ID пользователя должен быть {user_id}"

    def test_get_specific_user_by_string(self):
        """Получение информации о конкретном пользователе айди которого передан как строка"""
        user_id = "6"
        url = f'{self.base_url}/{user_id}'
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()['data']['id'] == int(user_id), f"ID пользователя должен быть {user_id}"

    def test_get_non_existent_user(self):
        """Получение информации о несуществующем пользователе"""
        non_existent_user_id = 666
        url = f'{self.base_url}/{non_existent_user_id}'
        response = requests.get(url)
        assert response.status_code == 404
        assert response.json() == {}, "При запросе несуществующего пользователя должен возвращаться пустой словарь"

    def test_api_users_not_get_method(self):
        """
        Получение информации о пользователях с использованием неверного метода, POST вместо GET. \n
        При использовании эндпоинта с POST методом происходит создание пользователя с уникальным айди и датой создания
        """

        current_time_before_request = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        response = requests.post(self.base_url)
        current_time_after_request = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        assert response.status_code == 201
        assert current_time_before_request <= response.json()['createdAt'] <= current_time_after_request, \
            "Время создания пользователя должно быть в временном промежутке между \n " \
            "current_time_before_request и current_time_after_request"


if __name__ == "__main__":
    pytest.main()
