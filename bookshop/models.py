from django.db import models
from mybook.models import Book
from django.contrib.auth.models import User



class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()


class UserShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books_to_buy = models.ManyToManyField(BookInventory, related_name='books_to_buy', blank=True)
