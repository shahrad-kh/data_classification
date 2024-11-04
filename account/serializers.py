from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from datasets.models import Dataset


class OperatorCreateSerializer(serializers.ModelSerializer):
    available_datasets = serializers.PrimaryKeyRelatedField(
        queryset=Dataset.objects.all(), many=True, required=False
    )
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default='operator')

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'available_datasets']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        profile_data = {
            'role': validated_data.pop('role', 'operator'),
            'available_datasets': validated_data.pop('available_datasets', [])
        }

        # Create the user
        user = User.objects.create_user(**validated_data)

        # Create a Profile if it doesn't already exist
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = profile_data['role']
        profile.available_datasets.set(profile_data['available_datasets'])
        profile.save()

        return user
    

class UpdateAvailableDatasetsSerializer(serializers.ModelSerializer):
    available_datasets = serializers.PrimaryKeyRelatedField(
        queryset=Dataset.objects.all(), many=True
    )

    class Meta:
        model = Profile
        fields = ['available_datasets']