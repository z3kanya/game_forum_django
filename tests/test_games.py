import pytest
from rest_framework import status
from django.urls import reverse

@pytest.mark.django_db
class TestGamesList:
    #TC-016, TC-017: Получение списка игр и поиск.

    def test_tc016_get_games_list_empty(self, api_client):
        # Если игр нет вернется пустой список
        url = reverse('game_list')
        response = api_client.get(url)
        assert response.status_code == 200
        if isinstance(response.data, list):
            assert response.data == []
        else:
            assert response.data['results'] == []


    def test_tc016_get_list_with_data(self, api_client, test_game):
        # Список содержит созданную игру
        url = reverse('game_list')
        response = api_client.get(url)
        assert response.status_code == 200
        games = response.data if isinstance(response.data, list) else response.data['results']
        assert len(games) >= 1
        titles = [game['name'] for game in games]
        assert 'Test Game' in titles


    def test_tc017_search_games_found(self, api_client, test_game):
        # Поиск игры по названию
        url = reverse('game_list') + '?search=Test'
        response = api_client.get(url)
        assert response.status_code == 200

        games = response.data if isinstance(response.data, list) else response.data['results']
        assert len(games) == 1
        assert games[0]['name'] == 'Test Game'

    def test_tc017_search_games_not_found(self, api_client, test_game):
        # Поиск игры по названию
        url = reverse('game_list') + '?search=NotFound'
        response = api_client.get(url)
        assert response.status_code == 200
        games = response.data if isinstance(response.data, list) else response.data['results']
        assert len(games) == 0