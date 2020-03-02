from django.contrib import admin

from core.models import StepikUser


@admin.register(StepikUser)
class StepikUserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    search_fields = ['id', 'full_name']
    list_filter = ['level_title']
    list_display = ['id', 'full_name', 'level_title', 'knowledge', 'reputation', 'solved_steps_count',
                    'issued_certificates_count']
