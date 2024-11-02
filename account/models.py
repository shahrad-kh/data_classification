from django.db import models
from django.contrib.auth.models import User
from datasets.models import Dataset


class Profile(models.Model):
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')
    available_datasets = models.ManyToManyField(Dataset, blank=True, related_name='operators')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    
    def save(self, *args, **kwargs):
        # Ensure that superusers have the admin role
        if self.user.is_superuser:
            self.role = 'admin'
            
        super().save(*args, **kwargs)
