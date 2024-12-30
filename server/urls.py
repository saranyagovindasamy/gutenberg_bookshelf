"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.utils.safestring import mark_safe

VERSION = "1.0.0"

schema_view = get_schema_view(
    openapi.Info(
        title="Gutenberg Book Shelf API",
        default_version="v1",
        description="API's for Gutenberg Book Shelf {}".format(VERSION),
        terms_of_service="URL",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

admin.site.site_header = mark_safe('SolomonAI API <span style="font-size: x-small">'
                                   f'({VERSION})</span>')
urlpatterns = [
 
    path('admin/', admin.site.urls),
    path("api/v1/", include("bookshelf.urls")),
    path("swagger/", schema_view.with_ui("swagger",
         cache_timeout=0), name="schema-swagger-ui"),
]
