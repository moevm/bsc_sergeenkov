from django.contrib import admin

from core.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
