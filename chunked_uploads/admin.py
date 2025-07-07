from django.contrib import admin
from .models import BookChunkedUpload

@admin.register(BookChunkedUpload)
class BookChunkedUploadAdmin(admin.ModelAdmin):
    list_display = ['upload_id', 'user', 'title', 'filename', 'offset', 'completed_at', 'is_scanned', 'is_clean']
    list_filter = ['is_scanned', 'is_clean', 'completed_at']
    search_fields = ['upload_id', 'title', 'filename', 'user__username']
    readonly_fields = ['upload_id', 'offset', 'completed_at']
