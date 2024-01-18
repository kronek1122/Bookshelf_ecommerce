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
    path('change_password/', views.UserPasswordChangeView.as_view(), name = 'change_password'),
    path('settings/', views.user_settings, name='user_settings'),
    path('delete_user/', views.delete_user, name='delete_user' ),
    path('change_user_data/', views.UserDataChangeView.as_view(), name = 'change_user_data'),
    path('change_user_data/done/', views.UserDataChangeDoneView.as_view(), name = 'change_user_data_done'),
    path('change_username/', views.UsernameChangeView.as_view(), name = 'change_username'),
    path('change_user_name/done/', views.UsernameChangeDoneView.as_view(), name = 'change_username_done'),
    path('search_result/', views.search_bar, name='search_result'),
]