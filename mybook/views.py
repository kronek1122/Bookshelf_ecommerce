from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from .models import Book


def home(request):
    return render(request, 'mybook/home.html')


@login_required
def user_view(request):
    return render(request, 'mybook/profile.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'mybook/signup.html'


class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    success_url = reverse_lazy('mybook:create_book')
    fields ='__all__'


class BookDetail(DetailView):
    model=Book


class BookList(ListView):
    model=Book
    context_object_name = 'book_list'