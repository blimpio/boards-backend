from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Card


class CardAdmin(BaseModelAdmin):
    list_display = ('name', 'type', 'board', 'created_by', 'featured')

admin.site.register(Card, CardAdmin)
