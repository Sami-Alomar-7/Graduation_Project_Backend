from rest_framework.views import APIView
from rest_framework import status, permissions, serializers
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_uploads.models import BookChunkedUpload
from books.models import Book
from books.seializers.book_upload_serializer import BookUploadSerializer
from store.models import Store
from store.serializers.store_serializer import StoreSerializer
from customer.models import Customer
from myadmin.models import Admin
from customer.permissions.customer_permission import IsCustomer
from myadmin.permissions.admin_permissions import IsAdmin
from utils.virus_scanner import virus_scanner
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError
import os

def validate_chunked_upload_file(value):
    """
    Validate that uploaded file is either epub or txt
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.epub', '.txt']
    
    if ext not in valid_extensions:
        raise serializers.ValidationError(
            f'Only {", ".join(valid_extensions)} files are allowed. '
            f'Uploaded file has extension: {ext}'
        )
    return value

class BookChunkedUploadView(ChunkedUploadView):
    """
    Handle chunked uploads for books
    """
    model = BookChunkedUpload
    field_name = 'file'
    
    def validate_chunk(self, chunk, upload):
        """Validate each chunk for file type"""
        # Only validate the first chunk (which contains the filename)
        if upload.offset == 0:
            validate_chunked_upload_file(chunk)
        return chunk
    
    def get_queryset(self, request):
        """Filter uploads by user"""
        return self.model.objects.filter(user=request.user)
    
    def create_chunked_upload(self, save=False, **kwargs):
        """Create a new chunked upload with user and metadata"""
        chunked_upload = self.model(
            user=self.request.user,
            **kwargs
        )
        if save:
            chunked_upload.save()
        return chunked_upload

class CustomerBookChunkedUploadView(BookChunkedUploadView):
    """
    Customer-specific chunked upload view
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def create_chunked_upload(self, save=False, **kwargs):
        """Create chunked upload for customer"""
        return super().create_chunked_upload(save, **kwargs)

class AdminBookChunkedUploadView(BookChunkedUploadView):
    """
    Admin-specific chunked upload view
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def create_chunked_upload(self, save=False, **kwargs):
        """Create chunked upload for admin"""
        return super().create_chunked_upload(save, **kwargs)

class BookChunkedUploadCompleteView(ChunkedUploadCompleteView):
    """
    Handle completion of chunked uploads with virus scanning
    """
    model = BookChunkedUpload
    
    def on_completion(self, chunked_upload, request):
        """
        Called when upload is completed
        """
        # Scan for viruses
        scan_result = virus_scanner.scan_file(chunked_upload.file.path)
        
        # Update scan results
        chunked_upload.is_scanned = True
        chunked_upload.is_clean = scan_result['clean']
        chunked_upload.scan_result = scan_result['result']
        chunked_upload.save()
        
        if not scan_result['clean']:
            # Delete the file if virus detected
            chunked_upload.delete()
            raise BadRequestError(
                en_message=f"Virus detected: {scan_result['result']}",
                ar_message=f"تم اكتشاف فيروس: {scan_result['result']}"
            )
        
        # Create the book
        user = request.user
        book_data = {
            'title': chunked_upload.title or 'Untitled Book',
            'author': chunked_upload.author or '',
            'description': chunked_upload.description or '',
            'file': chunked_upload.file,
        }
        
        try:
            if hasattr(user, 'customer'):
                # Customer upload
                customer_instance = Customer.objects.get(user=user)
                book = Book.objects.create(
                    customer=customer_instance,
                    admin=None,
                    **book_data
                )
                chunked_upload.book = book
                chunked_upload.save()
                
                return {
                    'book': BookUploadSerializer(book).data,
                    'scan_result': scan_result
                }
                
            elif user.role == 'ADMIN':
                # Admin upload
                admin_instance = Admin.objects.get(user=user)
                book = Book.objects.create(
                    customer=None,
                    admin=admin_instance,
                    **book_data
                )
                
                # Create store entry
                store_entry = Store.objects.create(
                    book=book,
                    admin=user,
                    status=Store.Status.PUBLIC
                )
                
                chunked_upload.book = book
                chunked_upload.save()
                
                return {
                    'book': BookUploadSerializer(book).data,
                    'store': StoreSerializer(store_entry).data,
                    'scan_result': scan_result
                }
            else:
                raise BadRequestError(
                    en_message="Invalid user role",
                    ar_message="دور المستخدم غير صالح"
                )
                
        except (Customer.DoesNotExist, Admin.DoesNotExist) as e:
            chunked_upload.delete()
            raise NotFoundError(
                en_message=f"Profile not found: {str(e)}",
                ar_message=f"لم يتم العثور على الملف الشخصي: {str(e)}"
            )
        except Exception as e:
            chunked_upload.delete()
            raise BadRequestError(
                en_message=f"Error creating book: {str(e)}",
                ar_message=f"خطأ في إنشاء الكتاب: {str(e)}"
            )

class CustomerBookChunkedUploadCompleteView(BookChunkedUploadCompleteView):
    """
    Customer-specific completion view
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

class AdminBookChunkedUploadCompleteView(BookChunkedUploadCompleteView):
    """
    Admin-specific completion view
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ChunkedUploadProgressView(APIView):
    """
    Get upload progress for a specific upload
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, upload_id):
        try:
            upload = BookChunkedUpload.objects.get(
                upload_id=upload_id,
                user=request.user
            )
        except BookChunkedUpload.DoesNotExist:
            raise NotFoundError(
                en_message="Upload not found",
                ar_message="لم يتم العثور على التحميل"
            )
        
        progress_data = {
            'upload_id': upload.upload_id,
            'filename': upload.filename,
            'offset': upload.offset,
            'total_size': upload.total_size,
            'status': upload.status,
            'completed_at': upload.completed_at,
            'is_scanned': upload.is_scanned,
            'is_clean': upload.is_clean,
            'scan_result': upload.scan_result,
            'progress_percentage': (upload.offset / upload.total_size * 100) if upload.total_size > 0 else 0
        }
        
        return ResponseFormatter.success_response(
            en="Upload progress retrieved successfully",
            ar="تم استرجاع تقدم التحميل بنجاح",
            data=progress_data
        )

class ChunkedUploadStopView(APIView):
    """
    Stop/cancel an ongoing upload
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, upload_id):
        try:
            upload = BookChunkedUpload.objects.get(
                upload_id=upload_id,
                user=request.user
            )
        except BookChunkedUpload.DoesNotExist:
            raise NotFoundError(
                en_message="Upload not found",
                ar_message="لم يتم العثور على التحميل"
            )
        
        # Only allow stopping if upload is still in progress
        if upload.status == 'uploading':
            # Delete the upload and associated files
            upload.delete()
            
            return ResponseFormatter.success_response(
                en="Upload stopped successfully",
                ar="تم إيقاف التحميل بنجاح",
                data={'upload_id': upload_id},
                status_code=status.HTTP_200_OK
            )
        else:
            raise BadRequestError(
                en_message="Cannot stop completed or failed upload",
                ar_message="لا يمكن إيقاف التحميل المكتمل أو الفاشل"
            )

class ChunkedUploadResumeView(APIView):
    """
    Resume an interrupted upload
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, upload_id):
        try:
            upload = BookChunkedUpload.objects.get(
                upload_id=upload_id,
                user=request.user
            )
        except BookChunkedUpload.DoesNotExist:
            raise NotFoundError(
                en_message="Upload not found",
                ar_message="لم يتم العثور على التحميل"
            )
        
        # Check if upload can be resumed
        if upload.status == 'uploading' and upload.offset < upload.total_size:
            resume_data = {
                'upload_id': upload.upload_id,
                'filename': upload.filename,
                'offset': upload.offset,
                'total_size': upload.total_size,
                'remaining_size': upload.total_size - upload.offset
            }
            
            return ResponseFormatter.success_response(
                en="Upload can be resumed",
                ar="يمكن استئناف التحميل",
                data=resume_data
            )
        else:
            raise BadRequestError(
                en_message="Upload cannot be resumed (already complete or failed)",
                ar_message="لا يمكن استئناف التحميل (مكتمل أو فاشل بالفعل)"
            )