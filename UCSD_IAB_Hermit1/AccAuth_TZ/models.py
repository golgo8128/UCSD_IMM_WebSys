
import pytz

from django.db import models
from django.contrib.auth.models import User # , AnonymousUser


class Hermit_Timezone(models.Model):
    
    timezone_pytz_str = models.CharField(default = "US/Pacific",
                                         max_length = 30,
                                         verbose_name = "Timezone",
                                         primary_key = True)  
    
    def tz(self):
        return pytz.timezone(self.timezone_pytz_str)   

    def __str__(self):
        return self.timezone_pytz_str

    class Meta:
        verbose_name        = 'Timezone (pytz)'
        verbose_name_plural = 'Timezones (pytz)'

    
class Hermit_User_TZ(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name = "User")
    
    timezone_obj = models.ForeignKey(Hermit_Timezone,
                                     on_delete=models.CASCADE,
                                     verbose_name = "Timezone")
    
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name        = "User's timezone"
        verbose_name_plural = "User's timezones"
