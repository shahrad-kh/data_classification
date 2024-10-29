from rest_framework import serializers
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
