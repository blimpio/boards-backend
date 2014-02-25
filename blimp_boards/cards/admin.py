from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Card


class CardAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'type', 'board', 'created_by', 'featured')
    prepopulated_fields = {
        'slug': ('name', )
    }


admin.site.register(Card, CardAdmin)
