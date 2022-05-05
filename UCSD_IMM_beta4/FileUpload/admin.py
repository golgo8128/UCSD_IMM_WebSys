from django.contrib import admin

# Register your models here.
from .models import FileUploaded, Project, DataType

admin.site.register(FileUploaded)
admin.site.register(Project)
admin.site.register(DataType)