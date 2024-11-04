import csv
from datetime import datetime

from django.db import transaction
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
from .serializers import (DatasetSerializer, FileUploadSerializer,
                          TagSerializer, TextSerializer)


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
    Displays Tag details by tag id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset  = Tag.objects.all()
    serializer_class = TagSerializer


class UpdateTagByIDAPIView(UpdateAPIView):
    """
    Update Tag fields by tag id
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DeleteTagByIDAPIView(DestroyAPIView):
    """
    Destroy Tag by tag id
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
    Displays Text details by text id
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
                action="update",
                updated_field="tags",
                action_details=action_description,
                datetime=datetime.now()
            )
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTextByIDAPIView(DestroyAPIView):
    """
    Destroy Text by text id
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
            Q(content__icontains=search_string)
        )

        # Serialize the results
        serializer = TextSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UploadCSVFileCreateAPIView(CreateAPIView):
    """
    Upload file to import data from csv file to database
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = FileUploadSerializer
    
    def post(self, request):
        print("start..")
        # Step 1: Validate the file input
        serializer = FileUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']

        try:
            # Step 2: Process the CSV data
            csv_reader = csv.DictReader(file.read().decode('utf-8').splitlines())

            with transaction.atomic():  # Ensure all-or-nothing on database actions
                for row in csv_reader:
                    # Extract fields from CSV row
                    dataset_name = row.get('dataset_name')
                    tags_names = row.get('tags_name', '').split(' ')
                    text_content = row.get('text_content')

                    if not dataset_name or not text_content:
                        return Response(
                            {"error": "Each row must contain 'dataset_name' and 'text_content'."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Step 3: Get or create the Dataset instance
                    dataset, created = Dataset.objects.get_or_create(name=dataset_name)
                    print("database created")
                    # Step 4: Get or create the Tag instances for this Dataset
                    tag_objects = []
                    for tag_name in tags_names:
                        tag_name = tag_name.strip()
                        
                        if tag_name:
                            tag, created = Tag.objects.get_or_create(
                            name=tag_name,
                            dataset=dataset,  # Ensure the tag is associated with the current dataset
                            defaults={'dataset': dataset}
                            )

                            # If tag already exists with a different dataset, raise an error
                            if not created and tag.dataset != dataset:
                                return Response(
                                    {"error": f"Tag '{tag_name}' is already associated with another dataset."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )

                        tag_objects.append(tag)
                        
                    print(tag_objects)
                    # Step 5: Check if a Text instance already exists for the same dataset and content
                    text_instance, created = Text.objects.update_or_create(
                        content=text_content,
                        dataset=dataset,
                    )

                    # Step 6: Associate tags with the Text instance
                    text_instance.tags.set(tag_objects)

            return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )