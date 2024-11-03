from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class Text(models.Model):
    content = models.TextField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"Text: {self.content[:50]}..."


class Log(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_instance = models.OneToOneField(Text, on_delete=models.CASCADE)
    action = models.TextField(max_length=20, blank=False, null=False, default="update")
    updated_field = models.TextField(max_length=10, blank=False, null=False, default="tags")
    action_details = models.TextField(max_length=300, blank=False, null=False, default="update")
    datetime = models.DateTimeField(default=datetime.now, blank=False, null=False)


    def __str__(self):
        return f"{self.user} - {self.user.profile.role} {self.action} on {self.text_instance} at {self.datetime}"
