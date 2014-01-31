from django.contrib import admin

from .models import Board, BoardCollaborator


admin.site.register([Board, BoardCollaborator])
