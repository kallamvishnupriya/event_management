from django.contrib import admin
from .models import OrganizerProfile


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'organization', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'organization']
    readonly_fields = ['created_at']
