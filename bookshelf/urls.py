from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

urlpatterns = [
   
 path('books/', BookListView.as_view(), name='book-list'),
]