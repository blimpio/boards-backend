from django.contrib import admin

from ..utils.admin import BaseModelAdmin
from .models import Card


class CardAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'position', 'type', 'board',
                    'created_by', 'featured')
    prepopulated_fields = {
        'slug': ('name', )
    }

    search_fields = ('name', 'slug', 'board__name', 'created_by__username', )


admin.site.register(Card, CardAdmin)
