from django.contrib import admin

from .models import Notification, NotificationSetting


class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'medium', 'send']


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('recipient__username', 'verb')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
