from django.contrib import admin
from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'chunk', 'book_title', 'age', 'role', 'created_at']
    list_filter = ['chunk__book', 'created_at', 'age', 'role']
    search_fields = ['name', 'hint', 'personality', 'chunk__book__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['chunk__book', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('chunk', 'name', 'hint', 'age', 'role', 'personality')
        }),
        ('Character Details', {
            'fields': ('physical_characteristics', 'events', 'relationships', 'aliases'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def book_title(self, obj):
        return obj.chunk.book.title
    book_title.short_description = 'Book'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('chunk__book')
