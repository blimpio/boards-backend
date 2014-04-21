from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Board, BoardCollaborator, BoardCollaboratorRequest


class BoardAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'account', 'created_by', 'is_shared', )
    search_fields = ('name', 'slug', 'account__name', 'created_by__username', )


class BoardCollaboratorAdmin(BaseModelAdmin):
    list_display = ('board', 'user', 'invited_user', 'permission', )
    search_fields = ('board__name', 'user__username', )


class BoardCollaboratorRequestAdmin(BaseModelAdmin):
    list_display = ('email', 'user', 'first_name', 'last_name', 'board', )
    search_fields = ('email', 'user__username', 'board__name', )


admin.site.register(Board, BoardAdmin)
admin.site.register(BoardCollaborator, BoardCollaboratorAdmin)
admin.site.register(BoardCollaboratorRequest, BoardCollaboratorRequestAdmin)
