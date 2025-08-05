from django.contrib import admin
from chunks.models import Chunk


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'chunk_index', 'chunk_size', 'created_at']
    list_filter = ['book', 'created_at']
    search_fields = ['book__title', 'chunk_text']
    readonly_fields = ['created_at', 'updated_at', 'chunk_size']
    ordering = ['book', 'chunk_index']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('book', 'chunk_index', 'chunk_text')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'chunk_size'),
            'classes': ('collapse',)
        }),
    )
    
    def chunk_size(self, obj):
        return obj.chunk_size
    chunk_size.short_description = 'Size (chars)'
