"""
Модели базового модуля.
Здесь могут быть общие модели, расширение модели User и т.д.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.db.models import Q

# Если нужна кастомная модель пользователя, раскомментируйте:
# class User(AbstractUser):
#     pass


class User(AbstractUser):
    # Модель пользователя


    avatar = models.ImageField(
        verbose_name='Аватарка',
        null=True,
        blank=True
    )

    tg_username = models.CharField(
    verbose_name='Username в Telegram',
    max_length=100,
    null=True,
    blank=True
    )

    telegram_chat_id = models.BigIntegerField(
        verbose_name='Chat ID Telegram',
        null=True,
        blank=True
    )


    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        help_text='Введите ваш email'
    )

    is_moderator = models.BooleanField(
        verbose_name='Модератор',
        default=False,
        help_text='Пользователь имеет права модератора'
    )

    can_create_news = models.BooleanField(
        verbose_name='Может создавать новости',
        default=False
    )

    can_edit_news = models.BooleanField(
        verbose_name='Может редактировать новости',
        default=False
    )

    can_delete_news = models.BooleanField(
        verbose_name='Может удалять новости',
        default=False
    )

    can_delete_comments = models.BooleanField(
        verbose_name='Может удалять комментарии',
        default=False
    )

    can_ban_1_day = models.BooleanField(
        verbose_name='Может банить на один день',
        default=False
    )

    appointed_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Назначен администратором',
        related_name='appointed_moderators'
    )


    last_activity = models.DateTimeField(
        verbose_name='Последняя активность',
        null=True,
        blank=True,
        help_text='Дата и время последней активности на сайте'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    

class AdminProfile(models.Model):
    # Модель администратора
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin',
        verbose_name='Админ',
        limit_choices_to={'is_superuser': True}
    )
    
    can_ban = models.BooleanField(
        verbose_name='Может выдавать баны',
        default=True
    )
    
    can_manage_moderators = models.BooleanField(
        verbose_name='Может управлять модераторами',
        default=True
    )
    
    can_view_statistics = models.BooleanField(
        verbose_name='Может просматривать статистику',
        default=True
    )

    manage_moderators = models.ManyToManyField(
        User,
        verbose_name='Назначенные модераторы',
        related_name='managed_by_admin',
        blank=True,
        limit_choices_to={'is_moderator': True}
    )
    

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self):
        return f'Администратор {self.user.username}'
    

    def promote_to_moderator(self, user, permissions):
        # Назначить права модератора

        if not self.can_manage_moderators:
            return False, "Нет прав на назначение модераторов"
        

        user.is_moderator = True
        user.can_create_news = permissions.get('can_create_news', False)
        user.can_edit_news = permissions.get('can_edit_news', False)
        user.can_delete_news = permissions.get('can_delete_news', False)
        user.can_delete_comments = permissions.get('can_delete_comments', False)
        user.can_ban_1_day = permissions.get('can_ban_1_day', False)
        user.appointed_by = self.user
        user.save()

        self.manage_moderators.add(user)
        self.save()

        return True, f"Пользователь {user.username} назначен модератором"
    
    def demote_moderator(self, user):
        # Снять права модератора
        if not self.can_manage_moderators:
            return False, "Нет прав на снятие модераторов"
        
        user.is_moderator = False
        user.can_create_news = False
        user.can_edit_news = False
        user.can_delete_news = False
        user.can_delete_comments = False
        user.can_ban_1_day = False
        user.appointed_by = None
        user.save()

        self.manage_moderators.remove(user)
        self.save()

        return True, f"У пользователя {user.username} сняты права модератора"
