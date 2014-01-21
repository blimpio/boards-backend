from django.contrib import admin

from .models import SignupRequest, InvitedUser


admin.site.register([SignupRequest, InvitedUser])
