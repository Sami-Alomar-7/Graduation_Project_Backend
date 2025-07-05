#rest 
from rest_framework import serializers
#models 
from myadmin.models import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"

class AdminMinimalSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for Admin model that includes only essential fields.
    Used when Admin data is needed as a nested object in other serializers.
    """
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    class Meta:
        model = Admin
        fields = ['id', 'full_name', 'email', 'phone']
        read_only_fields = fields  
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
