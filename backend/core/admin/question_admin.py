from django.contrib import admin

from core.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question']
    readonly_fields = ('id',)
