from rest_framework import status
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset, Tag, Text
from .serializers import DatasetSerializer, TagSerializer, TextSerializer


class DatasetListCreateAPIView(ListCreateAPIView):
    """
    Displays Dataset list or create new Dataset
    """
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class DatasetRetrieveAPIView(RetrieveAPIView):
    """
    Displays Dataset details by id
    """
    
    queryset  = Dataset.objects.all()
    serializer_class = DatasetSerializer


class DatasetUpdateAPIView(UpdateAPIView):
    """
    Update Dataset fields by id
    """
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    

class DatasetDestroyAPIView(DestroyAPIView):
    """
    Destroy Dataset by id
    """

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class CountTextByTagAPIView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all texts for this dataset
        texts = Text.objects.filter(dataset=dataset)

        # Group texts by tag and count occurrences
        tag_counts = {}
        for text in texts:
            for tag in text.tags.all():
                if tag.name not in tag_counts:
                    tag_counts[tag.name] = 0
                tag_counts[tag.name] += 1

        # Sort tags alphabetically
        sorted_tag_counts = dict(sorted(tag_counts.items()))

        return Response(sorted_tag_counts)
    

class TagListCreateAPIView(ListCreateAPIView):
    """
    Displays Tag list or create new Tag
    """
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveAPIView(RetrieveAPIView):
    """
    Displays Tag details by id
    """
    
    queryset  = Tag.objects.all()
    serializer_class = TagSerializer


class TagUpdateAPIView(UpdateAPIView):
    """
    Update Tag fields by id
    """
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDestroyAPIView(DestroyAPIView):
    """
    Destroy Tag by id
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TextListCreateAPIView(ListCreateAPIView):
    """
    Displays Text list or create new Text
    """
    
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    

class TextRetrieveAPIView(RetrieveAPIView):
    """
    Displays Text details by id
    """
    
    queryset  = Text.objects.all()
    serializer_class = TextSerializer
    
    
class TextUpdateAPIView(UpdateAPIView):
    """
    Update Text fields by id
    """
    
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    

class TextDestroyAPIView(DestroyAPIView):
    """
    Destroy Text by id
    """

    queryset = Text.objects.all()
    serializer_class = TextSerializer