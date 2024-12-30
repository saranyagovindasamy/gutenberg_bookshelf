from django.db import models

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'books_authors'

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        db_table = 'books_languages'


class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        db_table = 'books_subjects'


class Bookshelf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'books_bookshelfs'


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, null=True, blank=True)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    download_count = models.IntegerField(default=0)
    author = models.ManyToManyField(Author)
    subjects =  models.ManyToManyField(Subject)
    bookshelf = models.ManyToManyField(Bookshelf)
    gutenberg_id = models.IntegerField(primary_key=True)
    release_date = models.DateField()
    etext_no = models.IntegerField()
 
    class Meta:
        db_table = 'books_book'

    def __str__(self):
        return self.title


class BookFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_format'
    
    def __str__(self):
        return self.book.title