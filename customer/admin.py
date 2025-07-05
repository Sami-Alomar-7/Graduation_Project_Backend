from django.contrib import admin
from customer.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'get_phone')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'user__phone')
    list_per_page = 25

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'
