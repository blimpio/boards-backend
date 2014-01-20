from django.contrib import admin

from .models import Account, AccountMember, EmailDomain


admin.site.register([Account, AccountMember, EmailDomain])
