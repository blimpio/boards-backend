from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


def get_profile_fields(model_class, admin_class):
    """
    Returns a set of additional model fields that are not already in an
    admin site's fieldsets.
    """
    fields = []
    additional_fields = []

    for name, field_options in admin_class.fieldsets:
        fields.extend(list(field_options['fields']))

    for field in model_class._meta.fields:
        if field.name not in fields and field.name != 'id':
            additional_fields.append(field.name)

    return set(additional_fields)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': get_profile_fields(User, UserAdmin)}),
    )


admin.site.register(User, CustomUserAdmin)
