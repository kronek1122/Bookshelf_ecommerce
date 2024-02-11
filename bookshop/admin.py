from django.contrib import admin

from .models import BookInventory, UserShoppingCart


admin.site.register(BookInventory)
admin.site.register(UserShoppingCart)

