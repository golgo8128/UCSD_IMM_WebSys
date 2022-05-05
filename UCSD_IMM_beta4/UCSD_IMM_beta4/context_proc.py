
from django.conf import settings

def DIR_UCSD_IMM_WORK(request):
    return { 'DIR_UCSD_IMM_WORK': settings.UCSD_IMM_WORKDIR }