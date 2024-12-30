from django.db import models

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_author'


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)   
    gutenberg_id = models.PositiveIntegerField(unique=True)
    download_count = models.IntegerField(default=0)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name="books")
    subjects = models.ManyToManyField("Subject", through="BookSubject", related_name="books")
    bookshelves = models.ManyToManyField("Bookshelf", through="BookBookshelf", related_name="books")
    languages = models.ManyToManyField("Language", through="BookLanguage", related_name="books")

 
    class Meta:
        db_table = 'books_book'

    def __str__(self):
        return self.title
    

class Bookshelf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'books_bookshelf'

    def __str__(self):
        return self.name


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        db_table = 'books_language'

    def __str__(self):
        return self.code


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'books_subject'


class Format(models.Model):
    id = models.AutoField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.URLField(max_length=256)
    book = models.ForeignKey(Book, related_name="formats", on_delete=models.CASCADE)

    def __str__(self):
        return self.mime_type

    class Meta:
        db_table = 'books_format'
    

class BookSubject(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)

    class Meta:
        db_table = "books_book_subjects"


class BookBookshelf(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey("Bookshelf", on_delete=models.CASCADE)

    class Meta:
        db_table = "books_book_bookshelves"


class BookLanguage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "books_book_languages"