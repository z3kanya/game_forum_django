"""
Сериализаторы базового модуля.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from apps.games.serializers import GameSerializer


class RegisterSerializer(serializers.ModelSerializer):
    # Сериализатор регистрации новых пользователей
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        # валидация паролей и email
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'Пользователь с таким email уже существует'})

        return attrs
    
    def create(self, validated_data):
        # создание пользователя в базе данных, вызывается при serializer.save()
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    # Сериализатор профиля пользователя (для фронтенда)

    favorite_games = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'tg_username', 'date_joined', 'is_moderator', 'favorite_games')
        read_only_fields = ['id', 'date_joined', 'is_moderator']

    def get_favorite_games(self, obj):
        # Получение списка избранных игр
        from apps.games.models import FavoriteGame
        favorites = FavoriteGame.objects.filter(
            user=obj
        ).select_related('game')

        games = [favorite.game for favorite in favorites] # Создаем список игр

        return GameSerializer(games, many=True, context=self.context).data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # Сериализатор обновления профиля пользователя
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'tg_username', 'email')
        read_only_fields = ('username',)

     