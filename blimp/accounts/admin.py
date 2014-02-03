from django.contrib import admin

from .models import Account, AccountCollaborator, EmailDomain


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'allow_signup', )


class AccountCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'is_owner', )


admin.site.register(EmailDomain)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountCollaborator, AccountCollaboratorAdmin)
