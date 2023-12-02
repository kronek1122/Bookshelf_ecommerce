from django.urls import path

from . import views

app_name = 'mybook'
urlpatterns = [
    path('', views.home, name='home'),
    path('my_view', views.user_view, name='my_view'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]