from django.contrib import admin
from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'stepik_id']
    readonly_fields = ('id',)
