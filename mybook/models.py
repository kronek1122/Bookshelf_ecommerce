from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField()
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    isbn = models.CharField('ISBN',max_length=13,unique=True)
    genre = models.ManyToManyField(Genre)
    opinions = models.ManyToManyField('ReadBook', related_name='book_opinion')


    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class UserShelf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    read_books = models.ManyToManyField('Book', related_name='read_books', blank=True)
    to_read_books = models.ManyToManyField('Book', related_name='to_read_books', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Bookshelf"


class ReadBook(models.Model):
    shelf = models.ForeignKey(UserShelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read_date = models.DateField(null=True, blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.shelf.user.username} read {self.book.title} on {self.read_date}"
