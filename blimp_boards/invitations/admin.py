from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import SignupRequest, InvitedUser


class InvitedUserAdmin(BaseModelAdmin):
    readonly_fields = ('token', )
    search_fields = ('email', 'account__name', )


class SignupRequestAdmin(BaseModelAdmin):
    readonly_fields = ('token', )
    search_fields = ('email', )

admin.site.register(InvitedUser, InvitedUserAdmin)
admin.site.register(SignupRequest, SignupRequestAdmin)
