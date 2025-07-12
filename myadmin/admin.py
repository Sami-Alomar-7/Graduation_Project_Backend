from django.contrib import admin
from myadmin.models import Admin

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email')
    search_fields = ('user__email', 'user__username')
    list_per_page = 25

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
