from django.urls import path

from . import views


app_name = 'bookshop'
urlpatterns = [
    path('create_book/', views.BookInventory.as_view(), name='create_book'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),

]