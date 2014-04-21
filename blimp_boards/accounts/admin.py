from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Account, AccountCollaborator, EmailDomain


class AccountAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'allow_signup', )
    search_fields = ('name', 'slug', )


class AccountCollaboratorAdmin(BaseModelAdmin):
    list_display = ('user', 'account', 'is_owner', )
    search_fields = ('user__username', 'account__name', )


admin.site.register(EmailDomain)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountCollaborator, AccountCollaboratorAdmin)
