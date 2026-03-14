"""
Сериализаторы модуля новостей.
"""
from rest_framework import serializers
from .models import News, Comment
from apps.core.serializers import UserProfileSerializer


class NewsSerializer(serializers.ModelSerializer):
    # Сериализатор для новостей
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    class Meta:
        model = News
        fields = '__all__'

        # Только для чтения
        read_only_fields = ['author', 'views_count','created_at', 'updated_at', 'published_at', 'author_avatar']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем, есть ли лайк от текущего пользователя в связанных объектах news.likes
            return obj.likes.filter(user=request.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    # Сериализатор для комментариев
    author = UserProfileSerializer(read_only=True)

    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'created_at',
            'updated_at',
            'is_edited',
            'is_deleted',
            'can_edit',
            'can_delete'
        ]
        extra_kwargs = {
            'content': {'max_length': 1000} # ограничение на длину комментария
        }

        read_only_fields = ['author', 'created_at', 'updated_at', 'is_edited', 'is_deleted', 'news' ]

    def get_can_edit(self, obj):
        # Проверка, может ли пользователь редактировать комментарий
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id == obj.author.id
        return False
    
    def get_can_delete(self, obj):
        # Проверка, может ли пользователь удалить комментарий
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Пользователь может удалять свои комментарии
            if obj.author.id == request.user.id:
                return True
            # Модераторы и администраторы могут удалять любые комментарии
            if request.user.is_moderator:
                return True
            if request.user.is_superuser:
                return True
        return False 