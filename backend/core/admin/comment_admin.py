from django.contrib import admin

from core.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['text']
    readonly_fields = ('id',)
