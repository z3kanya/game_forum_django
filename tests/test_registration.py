import pytest


@pytest.mark.django_db
class TestRegistration:
    """Тесты регистрации"""
    REGISTER_URL = '/api/core/register/'

    def test_successful_registration(self, api_client):
        """Успешная регистрация пользователя."""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'TestPass123',
            'password2': 'TestPass123',
        }

        response = api_client.post(self.REGISTER_URL, data, format='json')
        assert response.status_code == 201

        json_data = response.json()
        assert json_data['success'] is True
        assert json_data['user']['username'] == 'newuser'
        assert json_data['user']['email'] == 'new@example.com'
        assert 'token' in json_data

    
    def test_existing_user(self, api_client, test_user):
        """Регистрация существующего пользователя"""
        data = {
            'username': test_user.username,
            'email': test_user.email,
            'password': 'TestPass123',
            'password2': 'TestPass123',
        }

        response = api_client.post(self.REGISTER_URL, data, format='json')
        assert response.status_code == 400
        assert 'username' in response.json()['errors']
    

    def test_password_mismatch(self, api_client):
        """Несовпадение паролей"""
        data = {
            'username': 'user',
            'email': 'example@example',
            'password': 'TestPass123',
            'password2': 'WrongPass123',
        }

        response = api_client.post(self.REGISTER_URL, data, format='json')
        assert response.status_code == 400
        assert 'password' in response.json()['errors']
    
    # Дописать...