#rest 
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
#serializers 
from authentication.serializers.user_serializers import (
    CustomTokenObtainPairSerializer, 
    RegisterSerializer,
    PasswordResetSerializer,
    PasswordResetRequestSerializer
)
from authentication.serializers.otp_serializers import (
    OTPVerificationSerializer,  
    ResendOTPSerializer, 
    PasswordResetVerifyOTPSerializer, 
)
#utils 
from authentication.utils import message, generate_random_otp
#django
from django.shortcuts import get_object_or_404
from django.utils import timezone
#tasks
from authentication.tasks import send_reset_password_verification_email_task
#models 
from authentication.models.user_model import User
from customer.models import Customer
from myadmin.models import Admin

#TODO add rate limit
class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        user_data = request.data
        serialized_data = RegisterSerializer(data = user_data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save() 
        return Response(serialized_data.data,HTTP_201_CREATED)
    @action(detail=False , methods=["POST"])
    def resend(self, request, *args,**kwargs):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            message(
                "OTP Sent",
                "تم إرسال الرمز", 
                "OK"
            ),
            HTTP_200_OK
        )
    @action(detail=False, methods=['post'])
    def verify(self, request, *args, **kwargs):
        serializerd_data = OTPVerificationSerializer(data=request.data)
        serializerd_data.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data.get("email"))
        if user.role == User.Role.CUSTOMER:
            Customer.objects.get_or_create(user=user)
        elif user.role == User.Role.ADMIN:
            Admin.objects.get_or_create(user=user) 
        response = message(
            "Email verified",
            "تم التحقق من الايميل",
            "OK"
        )
        return Response(response, HTTP_200_OK)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']        
        user = get_object_or_404(User, email=email)
        user.otp = generate_random_otp()
        user.otp_exp = timezone.now()
        user.save()
        send_reset_password_verification_email_task.delay(email, user.otp)
        return Response(
            message(
                "OTP Sent",
                "تم إرسال الرمز","success"
            ), 
            status=HTTP_200_OK
        )

class PasswordResetVerifyOTPView(APIView):
    def post(self, request):
        serializer = PasswordResetVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            message(
                en="OTP verified. Please enter your new password.", 
                ar="تم التأكد من الرمز، الرجاء ادخال كلمة المرور الجديدة", 
                status='success'
            ), 
            status=HTTP_200_OK
        )

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            message(
                en="Password has been reset successfully.", 
                ar="تم إعادة تعيين كلمة المرور بنجاح", 
                status="success"
            ),
            status=HTTP_200_OK
        )