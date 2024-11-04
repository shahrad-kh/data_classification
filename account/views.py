from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import (OperatorCreateSerializer,
                          UpdateAvailableDatasetsSerializer)


class CreateOperatorAPIView(APIView):
    """
    Create new operator: needs admin user permission
    fields: 
    username, 
    password, 
    role: admin - operator (default=operator), 
    available_datasets: list of IDs (could be blank)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access


    def post(self, request):
        serializer = OperatorCreateSerializer(data=request.data)

        # Check if data is valid
        if serializer.is_valid():
            serializer.save()  # Create the user and profile
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    """
    Login users
    fields: username, password
    """
    
    
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    Logout users
    """
    
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to log out


    def get(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class UpdateOperatorAvailableDatasetsAPIView(APIView):
    """
    Edit and Update operators available datasets: needs admin user permissions
    fields: 
    available_datasets: list of IDs
    """
    
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only admins can access


    def put(self, request, pk):
        try:
            # Retrieve the profile using the primary key
            profile = Profile.objects.get(pk=pk)
            
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate the incoming data
        serializer = UpdateAvailableDatasetsSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()  # Update available_datasets field
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
