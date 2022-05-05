from django.contrib import admin

# Register your models here.

from .models import Hermit_Timezone, Hermit_User_TZ

admin.site.register([ Hermit_Timezone,
                      Hermit_User_TZ ])