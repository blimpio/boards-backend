from django.contrib import admin

from .models import Account, AccountCollaborator, EmailDomain


admin.site.register([Account, AccountCollaborator, EmailDomain])
