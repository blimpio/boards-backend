from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from ..utils.admin import get_profile_fields
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    readonly_fields = ('token_version',)

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': get_profile_fields(User, UserAdmin)}),
    )


admin.site.register(User, CustomUserAdmin)
