from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import InactiveTagException
from .models import Dataset, Log, Tag, Text
from .permissions import (IsAdminOrCanEditLimitedFields,
                          IsAdminOrHasDatasetAccess)
from .serializers import DatasetSerializer, TagSerializer, TextSerializer


class CreateDatasetAPIView(CreateAPIView):
    """
    Create new Dataset
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class GetListOfDatasetsAPIView(ListAPIView):
    """
    Displays all Datasets
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class GetDetailOfDatasetByIDAPIView(RetrieveAPIView):
    """
    Displays Dataset details by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access
    
    queryset  = Dataset.objects.all()
    serializer_class = DatasetSerializer


class UpdateDatasetByIDAPIView(UpdateAPIView):
    """
    Update Dataset fields by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    

class DeleteDatasetByIDAPIView(DestroyAPIView):
    """
    Destroy Dataset by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access
    
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    

class CreateTagForDatasetByDatasetIDAPIView(APIView):
    """
    Create new Tag for specific Dataset by Dataset ID
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    
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
    permission_classes = [IsAuthenticated, IsAdminOrHasDatasetAccess]
    
    def get(self, request, pk):
        
        # Retrieve the Dataset by pk or return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Filter tags that belong to this dataset
        tags = Tag.objects.filter(dataset=dataset, is_active=True)
        serializer = TagSerializer(tags, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class GetDetailOfTagByIDAPIView(RetrieveAPIView):
    """
    Displays Tag details by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset  = Tag.objects.all()
    serializer_class = TagSerializer


class UpdateTagByIDAPIView(UpdateAPIView):
    """
    Update Tag fields by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DeleteTagByIDAPIView(DestroyAPIView):
    """
    Destroy Tag by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreateTextForDatasetByDatasetIDAPIView(APIView):
    """
    Create new Tag for specific Dataset by Dataset ID
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    
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
    permission_classes = [IsAuthenticated, IsAdminOrHasDatasetAccess]
    
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
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset  = Text.objects.all()
    serializer_class = TextSerializer
    
    
class UpdateTextByIDAPIView(UpdateAPIView):
    """
    API view to update a Text instance based on user role permissions.
    - Admins can update all fields of the Text instance.
    - Operators can only update `tags` field if they have access to the dataset.
    """

    permission_classes = [IsAuthenticated, IsAdminOrCanEditLimitedFields]
    serializer_class = TextSerializer
    
    def get_object(self):
        """
        Retrieve the Text instance using the primary key from URL kwargs.
        """
        
        pk = self.kwargs.get('pk')  # Retrieve pk from URL kwargs
        return get_object_or_404(Text, pk=pk)

    
    def put(self, request, *args, **kwargs):
        
        text_instance = self.get_object()

        # Check user role
        user = request.user
        is_operator = (hasattr(user, 'profile') and user.profile.role == 'operator')
        
        if is_operator:
            raise PermissionDenied("You don't have permission to do this action")
        
        serializer = self.get_serializer(text_instance, data=request.data)
        
        # Validate and save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, *args, **kwargs):
        """
        Handle full updates for a Text instance.
        """
        
        # Retrieve the Text instance
        text_instance = self.get_object()

        # Check user role
        user = request.user
        is_admin = user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

        # If user is an admin, allow updating all fields
        if is_admin:
            serializer = self.get_serializer(text_instance, data=request.data, partial=True)
        else:
            # For operators, filter data to only include `tags` field
            allowed_fields = {'tags'}
            limited_data = {key: value for key, value in request.data.items() if key in allowed_fields}
            
            # If the request contains fields outside of allowed ones, raise an error
            if set(request.data.keys()) - allowed_fields:
                raise PermissionDenied("You can only update 'tags' field.")
                
            serializer = self.get_serializer(text_instance, data=limited_data, partial=True)

        # Validate and save the data
        if serializer.is_valid():
            serializer.save()
            
            # Create a log entry for the operator's action
            action_description = f"Updated 'tags' field to {limited_data}"
            Log.objects.create(
                user=user,
                text_instance=text_instance,
                action=action_description,
                datetime=timezone.now()
            )
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTextByIDAPIView(DestroyAPIView):
    """
    Destroy Text by id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset = Text.objects.all()
    serializer_class = TextSerializer
    

class CountNumberOfTextLabeldByTagUsingDatasetIDAPIView(APIView):
    """
    Displays number of text labeld with unique Tag in specific Dataset
    """
    permission_classes = [IsAuthenticated, IsAdminOrHasDatasetAccess]
    
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
                if tag.is_active and tag.name not in tag_counts:
                    tag_counts[tag.name] = 0
                tag_counts[tag.name] += 1

        # Sort tags alphabetically
        sorted_tag_counts = dict(sorted(tag_counts.items()))

        return Response(sorted_tag_counts)


class FullTextSearchWithinTextsInDatasetByDatasetIDAPIView(APIView):
    """
    Search for texts within a specific dataset based on a query string.
    """
    permission_classes = [IsAuthenticated, IsAdminOrHasDatasetAccess]
    
    def get(self, request, pk, search_string):
        # Get the dataset by name or return 404 if it does not exist
        dataset = get_object_or_404(Dataset, pk=pk)

        # Filter texts that belong to this dataset and contain the search string
        texts = Text.objects.filter(dataset=dataset).filter(
            Q(content__icontains=search_string)  # Adjust 'content' to your actual field name
        )

        # Serialize the results
        serializer = TextSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)