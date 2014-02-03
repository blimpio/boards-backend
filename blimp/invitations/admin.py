from django.contrib import admin

from .models import SignupRequest, InvitedUser


class InvitedUserAdmin(admin.ModelAdmin):
    readonly_fields = ('token', )


class SignupRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('token', )

admin.site.register(InvitedUser, InvitedUserAdmin)
admin.site.register(SignupRequest, SignupRequestAdmin)
