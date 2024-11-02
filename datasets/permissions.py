from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from datasets.models import Text

from .models import Dataset


class IsAdminOrHasDatasetAccess(BasePermission):
    """
    Custom permission: grants access if the user is an admin or if they are an operator
    with access to the dataset in the URL parameter.
    """

    def has_permission(self, request, view):
        user = request.user

        # Allow access if the user is an admin
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'):
            return True

        # Check if the user is an operator and has access to the specific dataset
        if hasattr(user, 'profile') and user.profile.role == 'operator':
            # Extract the dataset ID from the URL path
            dataset_id = view.kwargs.get('pk') or view.kwargs.get('dataset_id')
            
            if dataset_id is not None:
                dataset = get_object_or_404(Dataset, pk=dataset_id)
                return dataset in user.profile.available_datasets.all()

        # Deny access if none of the above conditions are met
        return False


class IsAdminOrCanEditLimitedFields(BasePermission):
    """
    Custom permission: grants full access if the user is an admin.
    Operators can only edit certain fields if they have access to the dataset.
    """

    def has_permission(self, request, view):
        user = request.user
        # Allow access if the user is an admin
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'):
            return True

        # For operators, check if they have access to the dataset of the Text object
        if hasattr(user, 'profile') and user.profile.role == 'operator':
            # Extract the text ID from the URL path
            text_id = view.kwargs.get('pk')
            text = get_object_or_404(Text, pk=text_id)

            # Check if the operator has access to the dataset
            return text.dataset in user.profile.available_datasets.all()

        # Deny access if none of the above conditions are met
        return False

