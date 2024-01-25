from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    def get_opinions(self):
        return BookOpinion.objects.filter(book=self)


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

class BookOpinion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(UserShelf, on_delete=models.CASCADE)
    read_date = models.DateField(null=True, blank=True)
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.shelf.user.username} read {self.book.title} on {self.read_date}"


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciver')
    message = models.TextField()
    unread = models.BooleanField(default=True)
    time_stamp = models.TimeField(auto_now_add=True)


class UserFollow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    followers = models.ManyToManyField(User, related_name='following')
