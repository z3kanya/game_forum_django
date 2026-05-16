import pytest


class TestAuthentication:
    """Автотесты авторизации в систему (TC-006 - TC-010)"""
    LOGIN_URL = '/api/core/login/'

    def test_tc006_successful_login(self, api_client, test_user):
        """TC-006: Успешный вход в систему"""
        data = {
            'username': test_user.username,
            'password': 'TestPass123'
        }

        response = api_client.post(self.LOGIN_URL, data, format='json')

        assert response.status_code == 200

        json_data = response.json()

        assert json_data['success'] is True
        assert json_data['user']['username'] == test_user.username
        assert 'token' in json_data

    
    def test_tc007_wrong_password(self, api_client, test_user):
        """Вход с неверным паролем"""
        data = {
            'username': test_user.username,
            'password': 'WrongPass123'
        }

        response = api_client.post(self.LOGIN_URL, data, format='json')

        assert response.status_code == 401

        json_data = response.json()

        assert json_data['success'] is False

        assert 'errors' in json_data

    
    def test_tc008_nonexistent_user(self, api_client, db):
        """Вход с несуществующим пользователем"""
        data = {
            'username': 'nonexistentuser',
            'password': 'SomePass123'
        }


        response = api_client.post(self.LOGIN_URL, data, format='json')

        assert response.status_code == 401

        json_data = response.json()

        assert json_data['success'] is False
        assert 'errors' in json_data
        assert json_data['errors'] == 'Неправильное имя пользователя или пароль'


    def test_tc009_empty_fields(self, api_client):
        """Вход с пустыми полями"""
        data = {
            'username': '',
            'password': ''
        }

        response = api_client.post(self.LOGIN_URL, data, format='json')

        assert response.status_code == 400

        json_data = response.json()
        
        assert 'errors' in json_data
        assert json_data['errors'] == 'Пожалуйста, введите имя пользователя и пароль'

    
    def test_tc010_empty_password(self, api_client, test_user):
        """Вход с пустым паролем"""
        data = {
            'username': test_user.username,
        }

        response = api_client.post(self.LOGIN_URL, data, format='json')

        assert response.status_code == 400

        json_data = response.json()

        assert 'errors' in json_data
        assert json_data['errors'] == 'Пожалуйста, введите имя пользователя и пароль'

