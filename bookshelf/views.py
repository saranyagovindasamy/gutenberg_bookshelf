from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import *


class BookPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 100


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="ids",
                in_=openapi.IN_QUERY,
                description="Comma-separated Project Gutenberg ID numbers.",
                type=openapi.TYPE_STRING,
                required=False,
                examples=["1,2,3"]
            ),
            openapi.Parameter(
                name="language",
                in_=openapi.IN_QUERY,
                description="Comma-separated list of languages (e.g., 'en,fr').",
                type=openapi.TYPE_STRING,
                required=False,
                examples=["en,fr"]
            ),
            openapi.Parameter(
                name="author",
                in_=openapi.IN_QUERY,
                description="Filter by author's name. Partial matches supported (case insensitive).",
                type=openapi.TYPE_STRING,
                required=False,
                examples=["Mark Twain"]
            ),
            openapi.Parameter(
                name="title",
                in_=openapi.IN_QUERY,
                description="Filter by book title. Partial matches supported (case insensitive).",
                type=openapi.TYPE_STRING,
                required=False,
                examples=["Adventures"]
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                description="Page number for pagination.",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1
            ),
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                description="Number of books per page (max: 100).",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=25
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
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
    
    def get_queryset(self):
        queryset = Book.objects.all()

        language = self.request.query_params.get('language', None)
        if language:
            language_list = language.split(',')
            queryset = queryset.filter(languages__code__in=language_list)

        mime_type = self.request.query_params.get('mime_type', None)
        if mime_type:
            queryset = queryset.filter(download_links__format__icontains=mime_type)

        topic = self.request.query_params.get('topic', None)
        if topic:
            print("topic", topic)
            topics = topic.split(',')
            queries = Q()
            for t in topics:
                print(t)
                queries |= Q(subjects__name__icontains=t) | Q(bookshelves__name__icontains=t)
            queryset = queryset.filter(queries)
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