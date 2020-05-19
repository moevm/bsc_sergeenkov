from django.contrib import admin

from core.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['question__question', 'answer']
    readonly_fields = ('id',)
