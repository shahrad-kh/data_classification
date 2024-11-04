from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .exceptions import InactiveTagException
from .models import Dataset, Tag, Text


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'creation_date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'dataset', 'description', 'is_active']
        read_only_fields = ['dataset']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'content', 'dataset', 'tags']
        read_only_fields = ['dataset']
        
    def validate_tags(self, tags):
        # Iterate over each tag ID to check if the tag is active
        for tag in tags:
            if not tag.is_active:
                raise InactiveTagException(tag)
            
        return tags


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


    def validate_file(self, value):
        # Ensure the file has a .csv extension
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Uploaded file must be a CSV.")
        
        return value