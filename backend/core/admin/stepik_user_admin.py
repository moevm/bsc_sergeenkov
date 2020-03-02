from django.contrib import admin

from core.models import StepikUser


@admin.register(StepikUser)
class StepikUserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
