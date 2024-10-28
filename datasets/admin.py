from django.contrib import admin
from .models import Dataset, Tag, Text

# Register your models here.

admin.site.register(Dataset)
admin.site.register(Tag)
admin.site.register(Text)