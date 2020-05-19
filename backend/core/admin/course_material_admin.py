from django.contrib import admin

from core.models import CourseMaterial


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    search_fields = ['text']
    list_display = ['lesson_name', 'section_id', 'lesson_id', 'step_id', 'material_type']
    readonly_fields = ('id',)
