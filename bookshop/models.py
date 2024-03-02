from django.db import models
from mybook.models import Book
from django.contrib.auth.models import User



class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.book} store details"


class UserShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_inventory = models.ForeignKey(BookInventory, on_delete=models.CASCADE, default=None)
    quantity_in_cart = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} shopping cart"