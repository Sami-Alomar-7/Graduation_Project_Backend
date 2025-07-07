from django.urls import path
from chunked_uploads.views import (
    CustomerBookChunkedUploadView,
    AdminBookChunkedUploadView,
    CustomerBookChunkedUploadCompleteView,
    AdminBookChunkedUploadCompleteView,
    ChunkedUploadProgressView,
    ChunkedUploadStopView,
    ChunkedUploadResumeView
)

urlpatterns = [
    # Customer chunked uploads
    path('customer/book/chunk-upload/', CustomerBookChunkedUploadView.as_view(), name='customer-chunked-upload'),
    path('customer/book/chunk-upload/<uuid:upload_id>/', CustomerBookChunkedUploadCompleteView.as_view(), name='customer-chunked-upload-complete'),
    
    # Admin chunked uploads
    path('admin/book/chunk-upload/', AdminBookChunkedUploadView.as_view(), name='admin-chunked-upload'),
    path('admin/book/chunk-upload/<uuid:upload_id>/', AdminBookChunkedUploadCompleteView.as_view(), name='admin-chunked-upload-complete'),
    
    # Progress tracking
    path('book/chunk-upload/progress/<uuid:upload_id>/', ChunkedUploadProgressView.as_view(), name='upload-progress'),
    
    # Stop and resume uploads
    path('book/chunk-upload/stop/<uuid:upload_id>/', ChunkedUploadStopView.as_view(), name='upload-stop'),
    path('book/chunk-upload/resume/<uuid:upload_id>/', ChunkedUploadResumeView.as_view(), name='upload-resume'),
] 