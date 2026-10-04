from django.contrib import admin

from .models import AIInteraction


@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    list_display = ('feature', 'user', 'classroom', 'status', 'model_name', 'created_at')
    list_filter = ('feature', 'status', 'created_at')
    search_fields = ('user__username', 'classroom__name', 'error_message')
    readonly_fields = ('created_at',)
