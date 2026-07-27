import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.games.models import Game, Genre

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
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def test_genre(db):
    """Жанр в тестовой БД"""
    return Genre.objects.create(name='Action')


@pytest.fixture
def test_game(db, test_genre):
    """Игра в тестовой БД"""
    game = Game.objects.create(
        name='Test Game',
        version='1.0',
        developer='Test Developer',
        release_date='2022-01-01',
        min_requirements='Test Requirements',
        rec_requirements='Test Requirements',
        description='Test Description',
    )
    game.genres.add(test_genre)
    return game