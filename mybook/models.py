from django.db import models


class Genre(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField()
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    isbn = models.CharField('ISBN',max_length=13,unique=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"