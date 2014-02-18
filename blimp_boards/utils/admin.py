from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):

    def get_list_display(self, request):
        """
        Appends BaseModel's fields to ModelAdmin list_display.
        """
        return self.list_display + ('date_created', 'date_modified')
