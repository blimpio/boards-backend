from django.contrib import admin

from .models import Notification, NotificationSetting


class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'medium', 'send']


admin.site.register(Notification)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
