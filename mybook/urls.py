from django.urls import path

from . import views

app_name = 'mybook'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.user_view, name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('create_book/', views.BookCreate.as_view(), name='create_book'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book_detail'),
    path('books/', views.BookList.as_view(), name='book_list'),
]