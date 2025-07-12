from rest_framework.views import APIView
from rest_framework import status, permissions
from books.seializers.book_upload_serializer import BookUploadSerializer
from store.serializers.store_serializer import StoreSerializer
from store.models import Store
from customer.models import Customer
from myadmin.models import Admin
from customer.permissions.customer_permission import IsCustomer
from myadmin.permissions.admin_permissions import IsAdmin
from utils.virus_scanner import virus_scanner
from utils.messages import ResponseFormatter
from utils.api_exceptions import NotFoundError, BadRequestError

def scan_uploaded_file_or_error(uploaded_file):
    """
    Scan an uploaded file for viruses. Raise a custom API exception if infected.
    """
    result = virus_scanner.scan_django_file(uploaded_file)
    if not result['clean']:
        raise BadRequestError(
            en_message=f"Virus scan failed: {result['result']}",
            ar_message=f"فشل فحص الفيروسات: {result['result']}"
        )
    return True

class AdminBookUploadView(APIView):
    """
    Admin-specific book upload view that automatically adds books to the store
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def post(self, request, *args, **kwargs):
        serializer = BookUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Virus scan before saving
            uploaded_file = serializer.validated_data.get('file')
            scan_uploaded_file_or_error(uploaded_file)
            user = request.user
            try:
                admin_instance = Admin.objects.get(user=user)
            except Admin.DoesNotExist:
                raise NotFoundError(
                    en_message="Admin profile not found",
                    ar_message="لم يتم العثور على ملف المدير"
                )

            book = serializer.save(customer=None, admin=admin_instance)
            
            # Create store entry with PUBLIC status
            store_entry = Store.objects.create(
                book=book,
                admin=admin_instance,
                status=Store.Status.PUBLIC
            )
            
            response_data = {
                'book': BookUploadSerializer(book).data,
                'store': StoreSerializer(store_entry).data
            }
            
            return ResponseFormatter.success_response(
                en="Book uploaded successfully by admin and added to store",
                ar="تم رفع الكتاب بنجاح من قبل المدير وإضافته إلى المتجر",
                data=response_data,
                status_code=status.HTTP_201_CREATED
            )
        # Return detailed validation errors
        error_details = []
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                for error in errors:
                    error_details.append(f"{field}: {error}")
            else:
                error_details.append(f"{field}: {errors}")
        
        error_message = "; ".join(error_details)
        return ResponseFormatter.error_response(
            en=f"{error_message}",
            ar=f"{error_message}",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class CustomerBookUploadView(APIView):
    """
    Customer-specific book upload view
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = BookUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Virus scan before saving
            uploaded_file = serializer.validated_data.get('file')
            scan_uploaded_file_or_error(uploaded_file)
            user = request.user
            try:
                customer_instance = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                raise NotFoundError(
                    en_message="Customer profile not found",
                    ar_message="لم يتم العثور على ملف العميل"
                )
            
            book = serializer.save(customer=customer_instance, admin=None)
            
            response_data = {
                'book': BookUploadSerializer(book).data
            }
            
            return ResponseFormatter.success_response(
                en="Book uploaded successfully by customer",
                ar="تم رفع الكتاب بنجاح من قبل العميل",
                data=response_data,
                status_code=status.HTTP_201_CREATED
            )
        
        # Return detailed validation errors
        error_details = []
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                for error in errors:
                    error_details.append(f"{field}: {error}")
            else:
                error_details.append(f"{field}: {errors}")
        
        error_message = "; ".join(error_details)
        return ResponseFormatter.error_response(
            en=f"Validation errors: {error_message}",
            ar=f"أخطاء في التحقق: {error_message}",
            status_code=status.HTTP_400_BAD_REQUEST
        )