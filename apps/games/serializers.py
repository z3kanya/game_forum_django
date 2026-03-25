from PIL.ImageChops import screen
from rest_framework import serializers
from .models import Game, Genre, Language, FavoriteGame, Screenshot


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ['id', 'image']

class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    interface_language = LanguageSerializer(many=True, read_only=True)
    voice_language = LanguageSerializer(many=True, read_only=True)
    cover = serializers.ImageField(read_only=True)
    screenshots = ScreenshotSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'genres', 'version', 'developer', 'download_link',
            'interface_language', 'voice_language', 'release_date',
            'min_requirements', 'rec_requirements', 'description', 'created_at', 'cover', 'screenshots'
        ]

class GameShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'genres'] 


class FavoriteGameSerializer(serializers.ModelSerializer):
    game_details = GameSerializer(source='game', read_only=True)
    class Meta:
        model = FavoriteGame
        fields = '__all__'