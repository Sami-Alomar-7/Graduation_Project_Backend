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
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email']
        read_only_fields = fields  
