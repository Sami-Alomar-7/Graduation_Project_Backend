#rest
from rest_framework import serializers
#models 
from authentication.models import User
#django 
from utils import BadRequestError
#utils 
from authentication.utils import *
#django
from django.utils import timezone
#tasks
from authentication.tasks import send_verification_email_task

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    otp = serializers.CharField(max_length=6)
    def validate(self, attrs):
        if not User.objects.filter(email=attrs["email"],otp = attrs["otp"]).exists():
            raise BadRequestError(en_message="OTP is invalid",ar_message="OTP غير صحيح")
        user = User.objects.get(email=attrs["email"],otp = attrs["otp"])
        if user.is_otp_expired(): 
            raise BadRequestError(en_message="OTP EXPIRED",ar_message="انتهت فعالية الرمز")
        user.otp = None
        user.otp_exp = None     
        user.is_active = True
        user.save()   
        return super().validate(attrs)

class PasswordResetVerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6)
    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email'], otp=attrs['otp']).first()
        if not user:
            raise BadRequestError(en_message="OTP is invalid", ar_message="OTP غير صحيح")
        if user.is_otp_expired():
            raise BadRequestError(en_message="OTP EXPIRED", ar_message="انتهت فعالية الرمز")
        user.otp = None
        user.otp_exp = None
        user.save()
        return attrs

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise BadRequestError(en_message="No user is associated with this email address", ar_message="لا يوجد مستخدم مسجل بهذا الايميل")
        return value
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.otp = generate_random_otp()
        user.otp_exp = timezone.now()
        user.save()
        send_verification_email_task.delay(user.email, user.otp)
        return user