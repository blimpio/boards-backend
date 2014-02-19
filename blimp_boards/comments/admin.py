from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Comment


class CommentAdmin(BaseModelAdmin):
    list_display = ('__str__', 'created_by', 'content_type', 'content_object')

admin.site.register(Comment, CommentAdmin)
