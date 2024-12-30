from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import *

# Create your views here.
class BookPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 100

class BookListView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        queryset = Book.objects.all()

        # Filters

        language = self.request.query_params.getlist('language', None)
        if language:
            queryset = queryset.filter(language__in=language)

        mime_type = self.request.query_params.get('mime_type', None)
        if mime_type:
            queryset = queryset.filter(download_links__format__icontains=mime_type)

        topic = self.request.query_params.get('topic', None)
        if topic:
            print("topic", topic)
            queryset = queryset.filter(
                Q(subjects__name__icontains=topic) |
                Q(bookshelves__name__icontains=topic)
            )
            print(queryset)

        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(authors__name__icontains=author)

        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.order_by('-download_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "total": queryset.count(),
            "books": serializer.data
        })