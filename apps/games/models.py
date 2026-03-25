from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Язык")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название игры', 
    )
    genres = models.ManyToManyField(
        Genre, 
        related_name='games', 
        verbose_name="Жанры" 
    )
    version = models.CharField(
        max_length=30,
        verbose_name='Версия', 
    )
    developer = models.CharField(
        max_length=255,
        verbose_name='Разработчик', 
    )
    release_date = models.CharField(
        max_length=100, 
        verbose_name="Дата выпуска"
    )
    interface_language = models.ManyToManyField(
        Language,
        related_name='games_interface', 
        verbose_name='Язык интерфейса', 
    )
    voice_language = models.ManyToManyField(
        Language,
        related_name='games_voice', 
        verbose_name='Язык озвучивания', 
    )
    min_requirements = models.TextField(
        verbose_name='Минимальные системные требования', 
    )
    rec_requirements = models.TextField(
        verbose_name='Рекомендуемые системные требования', 
    )
    description = models.TextField(
        verbose_name='описание'
    )

    download_link = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Ссылка на скачивание"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    
    cover = models.ImageField(
        upload_to='games/covers',
        blank=True,
        null=True,
        verbose_name="Обложка"
    ) 

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class FavoriteGame(models.Model):
    # Избранные игры пользователя
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_games',
        verbose_name='Пользователь'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Игра'
    )

    class Meta:
        verbose_name = "Избранная игра"
        verbose_name_plural = "Избранные игры"
        unique_together = ['user', 'game']

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
    
class Screenshot(models.Model):
    # Скриншоты игры
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='screenshots',
        verbose_name='Игра'
    )
    image = models.ImageField(
        upload_to='games/screenshots',
        verbose_name='Изображение'
    )


    class Meta:
        verbose_name = "Скриншот"
        verbose_name_plural = "Скриншоты"