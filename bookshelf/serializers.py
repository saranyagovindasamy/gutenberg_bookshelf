from .models import *
from rest_framework import serializers


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code']


class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'birth_year','death_year','name']


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['id', 'name']


class BookFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['id', 'mime_type', 'url', 'book_id']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    formats = BookFormatSerializer(many=True, read_only=True)
    subjects = serializers.StringRelatedField(many=True, read_only=True, source="subject_set")
    bookshelves = serializers.StringRelatedField(many=True, read_only=True, source="bookshelf_set")
    languages = serializers.StringRelatedField(many=True, read_only=True, source="language_set")

    class Meta:
        model = Book
        fields = [
            "id", "title", "download_count", "gutenberg_id", "media_type",
            "authors", "subjects", "bookshelves", "languages", "formats"
        ]

