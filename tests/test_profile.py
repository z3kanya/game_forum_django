import pytest


@pytest.mark.django_db
class TestProfile:
    """Автотесты профиля пользователя (TC-011 - TC-015)"""

    PROFILE_URL = '/api/core/profile/'
    UPDATE_URL = '/api/core/profile/update/'

    def test_tc011_get_profile(self, auth_client, test_user):
        """Получение профиля авторизованного пользователя"""
        response = auth_client.get(self.PROFILE_URL)
        assert response.status_code == 200

        json_data = response.json()

        assert json_data['username'] == test_user.username
        assert json_data['email'] == test_user.email

        assert 'id' in json_data
        assert 'date_joined' in json_data
        assert 'is_moderator' in json_data

    def test_tc012_get_profile_unauthorized(self, api_client):
        """Получение профиля неавторизованного пользователя"""
        response = api_client.get(self.PROFILE_URL)
        assert response.status_code in [401, 403]

        json_data = response.json()

        assert 'detail' in json_data

    def test_tc013_update_profile(self, auth_client, test_user):
        """Смена имени в профиля авторизованного пользователя"""
        data = {
            'first_name': 'Testname'
        }

        response = auth_client.patch(self.UPDATE_URL, data, format='json')

        assert response.status_code == 200

        json_data = response.json()

        assert json_data['first_name'] == 'Testname'
        assert 'username' in json_data
        assert 'email' in json_data


    def test_tc014_download_avatar(self, auth_client):
        """Загрузка аватара"""
        from django.core.files.uploadedfile import SimpleUploadedFile

        avatar = SimpleUploadedFile(
            name='avatar.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )

        response = auth_client.patch(self.UPDATE_URL, {'avatar': avatar}, format='multipart')

        assert response.status_code == 200

        json_data = response.json()

        assert 'avatar' in json_data
        assert json_data['avatar'] is not None



    def test_tc015_update_profile_unauthorized(self, api_client):
        """Смена имени в профиля неавторизованного пользователя"""
        data = {
            'first_name': 'Hacker'
        }

        response = api_client.patch(self.UPDATE_URL, data, format='json')

        assert response.status_code in [401, 403]

        json_data = response.json()

        assert 'detail' in json_data