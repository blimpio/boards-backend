from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    filter_horizontal = ()
    readonly_fields = ('token_version',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),

        (_('Additional data'), {
            'fields': ('job_title', 'avatar_path', 'gravatar_url', 'last_ip',
                       'timezone', 'token_version', 'last_login')
        }),
    )


admin.site.register(User, CustomUserAdmin)
