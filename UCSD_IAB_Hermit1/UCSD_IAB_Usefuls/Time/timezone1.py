#!/usr/bin/env python

import dateutil.parser
import pytz

import django
from django.conf import settings

from AccAuth_TZ.models import Hermit_User_TZ, Hermit_Timezone

try:
    TIME_ZONE_THISSERVER = settings.TIME_ZONE_THISSERVER
except django.core.exceptions.ImproperlyConfigured:
    TIME_ZONE_THISSERVER = "US/Pacific"

# pytz.timezone("US/Pacific").localize(dateutil.parser.parse("2016/03/01 23:15"))

def get_tzone(django_user):
    
    if django_user.is_anonymous:
        return pytz.timezone(TIME_ZONE_THISSERVER)
    else:
        return Hermit_User_TZ.objects.get(user = django_user).timezone_obj.tz()
    
