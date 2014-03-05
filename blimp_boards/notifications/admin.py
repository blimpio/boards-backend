from django.contrib import admin

from .models import Notification, NotificationType, NotificationSetting


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'display', 'description']


class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'medium', 'send']


admin.site.register(Notification)
admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(NotificationSetting, NotificationSettingAdmin)
