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
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone']
        read_only_fields = fields  
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
