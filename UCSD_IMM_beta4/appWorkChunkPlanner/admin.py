from django.contrib import admin

# Register your models here.

from .models import WorkChunk_Class, WorkChunk_Type, \
    WorkChunk_Project, WorkChunk_Plan, WorkChunk_Plan_Status, \
    WorkChunk_Record,  WorkChunk_Served, \
    WorkChunk_Plan_Link_Type, WorkChunk_Plan_Link
    
admin.site.register([ WorkChunk_Class,
                      WorkChunk_Type,
                      WorkChunk_Project,
                      WorkChunk_Plan,
                      WorkChunk_Plan_Status,
                      WorkChunk_Record,
                      WorkChunk_Served,
                      WorkChunk_Plan_Link_Type,
                      WorkChunk_Plan_Link ])