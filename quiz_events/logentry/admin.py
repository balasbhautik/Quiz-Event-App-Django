from django.contrib import admin
from logentry.models import LogEntry

# Register your models here.

@admin.register(LogEntry)
class LogEntryModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','ip_address','api_name', 'api_type','date_time']
    search_fields = ['user','api_name','api_type','date_time']
    readonly_fields = ['id', 'user', 'ip_address', 'api_name', 'api_type', 'date_time']

    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    