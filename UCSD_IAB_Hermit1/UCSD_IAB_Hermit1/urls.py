"""UCSD_IAB_Hermit1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path(r'app/NichoAnu/',
         include("appNichoAnu.urls", namespace="appNichoAnu")),

    path(r'login/', include("AccAuth_TZ.urls", namespace="AccAuth_TZ")),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL,
           document_root = settings.MEDIA_ROOT)

# https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-uploaded-files-in-development
#
# ### Serving files uploaded by a user during development ###
#
# During development, you can serve user-uploaded media files from MEDIA_ROOT using the django.views.static.serve() view.
# This is not suitable for production use! For some common deployment strategies, see Deploying static files.
# For example, if your MEDIA_URL is defined as /media/, you can do this by adding the following snippet to your urls.py:
#
# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# Note: This helper function works only in debug mode and only if the given prefix is local
# (e.g. /media/) and not a URL (e.g. http://media.example.com/).

