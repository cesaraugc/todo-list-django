from rest_framework import serializers
from .models import List, Item

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model=List
        fields = ['title']
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields = ('title', 'description', 'list', 'created_by')