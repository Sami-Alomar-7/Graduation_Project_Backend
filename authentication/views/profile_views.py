from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from authentication.serializers import UserProfileSerializer
from utils.messages import ResponseFormatter

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    def get_object(self):
        return self.request.user
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseFormatter.success_response(
            en="Profile retrieved successfully",
            ar="تم استرجاع الملف الشخصي بنجاح",
            data=serializer.data
        )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ResponseFormatter.success_response(
            en="Profile updated successfully",
            ar="تم تحديث الملف الشخصي بنجاح",
            data=serializer.data
        ) 