from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Добавляем поле avatar в форму редактирования и создания
    fieldsets = UserAdmin.fieldsets + (
        ('Аватар', {'fields': ('avatar',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Аватар', {'fields': ('avatar',)}),
    )
    # Опционально: показываем миниатюру в списке пользователей
    list_display = UserAdmin.list_display + ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" />'
        return '-'
    avatar_preview.allow_tags = True
    avatar_preview.short_description = 'Аватар'


admin.site.register(User, CustomUserAdmin)
