from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset, Tag, Text
from .serializers import DatasetSerializer, TagSerializer, TextSerializer


class CreateDatasetAPIView(CreateAPIView):
    """
    Create new Dataset
    """
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class GetListOfDatasetsAPIView(ListAPIView):
    """
    Displays all Datasets
    """
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class GetDetailOfDatasetByIDAPIView(RetrieveAPIView):
    """
    Displays Dataset details by id
    """
    
    queryset  = Dataset.objects.all()
    serializer_class = DatasetSerializer


class UpdateDatasetByIDAPIView(UpdateAPIView):
    """
    Update Dataset fields by id
    """
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    

class DeleteDatasetByIDAPIView(DestroyAPIView):
    """
    Destroy Dataset by id
    """

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    

class CreateTagForDatasetByDatasetIDAPIView(APIView):
    """
    Create new Tag for specific Dataset by Dataset ID
    """
    
    def post(self, request, pk):
        
        # Retrieve the Dataset by pk or return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Create the Tag instance with dataset as a foreign key
        serializer = TagSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(dataset=dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetListOfTagsOfDatasetByDatasetIDAPIView(APIView):
    """
    Displays all Tags of a Dataset by Dataset ID
    """
    
    def get(self, request, pk):
        
        # Retrieve the Dataset by pk or return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Filter tags that belong to this dataset
        tags = Tag.objects.filter(dataset=dataset)
        serializer = TagSerializer(tags, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class GetDetailOfTagByIDAPIView(RetrieveAPIView):
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


class CreateTextForDatasetByDatasetIDAPIView(APIView):
    
    def post(self, request, pk):
        
        # Retrieve the Dataset by pk or return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Create the Text instance with dataset as a foreign key
        serializer = TextSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(dataset=dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetListOfTextsOfDatasetByDatasetIDAPIView(APIView):
    """
    Displays all Texts of a Dataset by Dataset ID
    """
    
    def get(self, request, pk):
        
        # Retrieve the Dataset by pk or return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Filter texts that belong to this dataset
        texts = Text.objects.filter(dataset=dataset)
        serializer = TextSerializer(texts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetDetailOfTextByIDAPIView(RetrieveAPIView):
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
    

class CountTextByTagAPIView(APIView):
    """
    Displays number of text labeld with unique Tag
    """
    
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


class TextSearchAPIView(APIView):
    """
    Search for texts within a specific dataset based on a query string.
    """

    def get(self, request, dataset_name, search_string):
        # Get the dataset by name or return 404 if it does not exist
        dataset = get_object_or_404(Dataset, name=dataset_name)

        # Filter texts that belong to this dataset and contain the search string
        texts = Text.objects.filter(dataset=dataset).filter(
            Q(content__icontains=search_string)  # Adjust 'content' to your actual field name
        )

        # Serialize the results
        serializer = TextSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)