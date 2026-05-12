import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    """Неавторизованный клиент для запросов."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Пользователь в тестовой БД"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPass123',
    )


@pytest.fixture
def auth_client(api_client, test_user):
    """Клиент с авторизацией через JWT."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client
