#rest 
from rest_framework import serializers
#models 
from customer.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerMinimalSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for Customer model that includes only essential fields.
    Used when Customer data is needed as a nested object in other serializers.
    """
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email']
        read_only_fields = fields  