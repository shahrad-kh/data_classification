from django.contrib import admin
from .models import Dataset, Tag, Text, Log


admin.site.register(Dataset)
admin.site.register(Tag)
admin.site.register(Text)
admin.site.register(Log)