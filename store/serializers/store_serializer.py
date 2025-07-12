from rest_framework import serializers
from store.models import Store
from books.models import Book
from myadmin.models import Admin

class StoreSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    admin = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.all())

    class Meta:
        model = Store
        fields = '__all__'