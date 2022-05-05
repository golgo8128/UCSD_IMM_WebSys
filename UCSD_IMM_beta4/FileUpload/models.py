
import os
from django.conf import settings
from django.db import models

# Create your models here.

from django.contrib.auth.models import User # , AnonymousUser

# print(dir(settings))

#
# http://stackoverflow.com/questions/937954/how-do-you-specify-a-default-for-a-django-foreignkey-model-or-adminmodel-field
#

class Project(models.Model):
	projname = models.CharField("Project name", max_length=100, unique = True)

	def __str__(self):
		return self.projname

class DataType(models.Model):
	datatype = models.CharField("Data type", max_length=100, unique = True)
	# File type (raw GC-MS, table, etc.)
	
	def __str__(self):
		return self.datatype


class FileUploaded(models.Model):
	ifile = models.FileField("Uploaded file", upload_to = os.path.join(settings.MEDIA_ROOT,
							 'FilesUploaded/Ver0p1/%Y/%m/%d'), max_length=500)
	iproj = models.ForeignKey(Project, verbose_name = "Project name")
	idatatype = models.ForeignKey(DataType, verbose_name = "Data type")
	idescription = models.CharField("Brief file description", max_length=2000)
	ifilename = models.CharField("Original file name", max_length=500)
	itimestamp_upload = models.DateTimeField("Time uploaded")
	itimestamp_touch  = models.DateTimeField("Time used")
	iuser = models.ForeignKey(User, verbose_name = "Uploaded user") # on_delete=models.SET_NULL??

	def __str__(self):
		return "%s[%s]: %s" % (self.iproj.projname, self.idatatype.datatype, self.ifilename)

