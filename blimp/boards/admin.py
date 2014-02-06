from django.contrib import admin

from .models import Board, BoardCollaborator


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'created_by', 'is_shared', )


class BoardCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'invited_user', 'permission', )


admin.site.register(Board, BoardAdmin)
admin.site.register(BoardCollaborator, BoardCollaboratorAdmin)
