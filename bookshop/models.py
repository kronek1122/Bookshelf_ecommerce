from django.db import models
from mybook.models import Book


class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
