from django.contrib import admin

from .models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'created_by', 'is_shared', )


class BoardCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'invited_user', 'permission', )


class BoardCollaboratorRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'first_name', 'last_name', 'board', )


admin.site.register(Board, BoardAdmin)
admin.site.register(BoardCollaborator, BoardCollaboratorAdmin)
admin.site.register(BoardCollaboratorRequest, BoardCollaboratorRequestAdmin)
