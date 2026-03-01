from django.contrib import admin
from .models import Travel


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'location', 'cost', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
