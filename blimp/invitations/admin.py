from django.contrib import admin

from .models import InviteRequest, InvitedUser


admin.site.register([InviteRequest, InvitedUser])
