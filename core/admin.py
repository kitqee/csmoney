from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = RegisterForm
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'birthday', 'about_me')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )

    list_display = ['phone', 'is_superuser', 'last_login']
    list_display_links = ['phone']
    search_fields = ['phone', 'first_name', 'last_name']
    ordering = ['phone']
    readonly_fields = ['last_login', 'date_joined']
