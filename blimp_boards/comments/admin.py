from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Comment


class CommentAdmin(BaseModelAdmin):
    list_display = ('__str__', 'created_by', 'content_type', 'content_object')
    search_fields = ('created_by__username', )

admin.site.register(Comment, CommentAdmin)
