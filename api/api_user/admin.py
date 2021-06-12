from django.contrib import admin
from django.contrib.auth import admin as upstream
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import CustomUser


class UserAdmin(upstream.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email')}
         ),
    )
    form = UserChangeForm
    add_form = UserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
