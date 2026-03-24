from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import News, Comment, NewsLike
from .serializers import NewsSerializer, CommentSerializer
from django.conf import settings
import telebot
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django.db.models import Count


User = get_user_model()

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


class IsModeratorUser(permissions.BasePermission):
    # Разрешение для модераторов (нужно для создания постов)
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_moderator:
            return True
        return False



class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.annotate(likes_count_attr=Count('likes')).all()
    serializer_class = NewsSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_at', 'likes_count_attr', 'views_count']
    ordering = ['-published_at']

    def get_permissions(self):
        if self.request.method == 'OPTIONS':
            return [permissions.AllowAny()]
        # Проверка разрешений для публикации новости
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser | IsModeratorUser]
        elif self.action == 'like':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]

        return super().get_permissions()
    



    def perform_create(self, serializer):
        # Публикация новости
        news = serializer.save(
            author=self.request.user,
            is_published=True,
            published_at=timezone.now()
        )

        print("Новость создана:", news.title)
        self._send_telegram(news)

    
    def perform_update(self, serializer):
        # Обновление новости
        news = serializer.save()

    
    def perform_destroy(self, instance):
        # Удаление новости
        instance.delete()

    
    def _send_telegram(self, news):
        # Отправка новости в Telegram

        print("Запущена рассылка")
        subscribers = User.objects.exclude(telegram_chat_id__isnull=True).exclude(telegram_chat_id='')

        if not subscribers.exists():
            return
        
        text = f"""{news.title}
        {news.short_description}
        Читать: https://127.0.0.1:3000
        """

        for user in subscribers:
            try:
                bot.send_message(user.telegram_chat_id, text)
            except Exception as e:
                print(f"Ошибка отправки {user.telegram_chat_id}: {e}")

                if "chat not found" in str(e).lower():
                    user.telegram_chat_id = None
                    user.save()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Лайк новости
        news = self.get_object()
        like, created = NewsLike.objects.get_or_create(
            news=news,
            user=request.user
        )

        if not created:
            like.delete() # Повторное нажатие убирает лайк
            liked = False
        else:
            liked = True

        return Response({
            'liked': liked,
            'likes_count': news.likes.count()
        })

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        """Эндпоинт для работы с комментариями конкретной новости"""
        news = self.get_object() # Получаем новость по ID из URL

        if request.method == 'GET':
            # Получаем все активные комментарии для этой новости
            comments = news.comments.filter(is_deleted=False)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            # Создаем новый комментарий
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    author=request.user,
                    news=news
                )
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class CommentView(viewsets.ModelViewSet):
    # Класс для работы с комментариями
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        # 1. ОБЯЗАТЕЛЬНО: OPTIONS должен быть доступен всем для работы CORS
        if self.request.method == 'OPTIONS':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        # 2. Безопасное получение news_pk
        news_pk = self.kwargs.get('news_pk')
        if not news_pk:
            return Comment.objects.none()
            
        return Comment.objects.filter(
            news_id=news_pk,
            is_deleted=False
        ).select_related('author', 'news')

    def perform_create(self, serializer):
        # 3. Проверка существования новости перед сохранением
        news_pk = self.kwargs.get('news_pk')
        try:
            news = News.objects.get(pk=news_pk)
            serializer.save(author=self.request.user, news=news)
        except News.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"detail": "Новость не найдена"})

    # def get_queryset(self):
    #     # Получение списка комментов к новости
    #     return Comment.objects.filter(
    #         news_id=self.kwargs.get('news_pk'),
    #         is_deleted=False
    #     ).select_related('author', 'news') # Подгрузка связанных объектов (чтобы не загружать весь объект новости)
    

    # def get_permissions(self):
    #     # Проверка прав для работы с комментариями
    #     if self.request.method == 'OPTIONS':
    #         return [permissions.AllowAny()]

    #     if self.action == 'create':
    #         self.permission_classes = [permissions.IsAuthenticated]
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         self.permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         self.permission_classes = [permissions.AllowAny]

    #     return super().get_permissions()
    
    # def perform_create(self, serializer):
    #     # Создание комментария
    #     news = News.objects.get(pk=self.kwargs['news_pk'])
    #     serializer.save(
    #         author=self.request.user,
    #         news=news
    #     )

    
    def perform_update(self, serializer):
        # Обновление комментария
        comment = self.get_object()
        if comment.author.id != self.request.user.id:
            self.permission_denied(self.request, "Только автор может редактировать свои комментарии")

        serializer.save(is_edited=True)


    def perform_destroy(self, instance):
        # Удаление комментария
        can_delete = (
            instance.author.id == self.request.user.id
            or self.request.user.is_moderator
            or self.request.user.is_superuser
        )

        if not can_delete:
            self.permission_denied(self.request, "Только автор может удалять свои комментарии")

        instance.delete()