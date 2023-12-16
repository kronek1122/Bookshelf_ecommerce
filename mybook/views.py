from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from .models import Book, UserShelf
from .forms import AddToShelfForm


def home(request):
    return render(request, 'mybook/home.html')


@login_required
def user_view(request):
    try:
        user_shelf = UserShelf.objects.get(user=request.user)

        read_books = user_shelf.read_books.all()
        to_read_books = user_shelf.to_read_books.all()

        context = {
            'read_books': read_books,
            'to_read_books': to_read_books,
        }
    except:
        context = {
            'read_books': 'empty',
            'to_read_books': 'empty',
        }

    return render(request, 'mybook/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('/mybook/settings')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mybook/change_password.html', {
        'form':form
    })


def user_settings(request):
    return render(request, 'mybook/setting_page.html')


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
    context_object_name = 'book_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['object']
        context['genres'] = book.genre.all()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'add_to_read':
            self.add_book_to_shelf('read', 'Read')
        elif action == 'add_to_to_read':
            self.add_book_to_shelf('to_read', 'To Read')
        else:
            messages.warning(request, 'Invalid action.')

        return redirect('mybook:book_detail', pk=self.kwargs['pk'])

    def add_book_to_shelf(self, status, shelf_name):
        book = self.get_object()
        user_shelf, created = UserShelf.objects.get_or_create(user=self.request.user)

        if status == 'read':
            user_shelf.read_books.add(book)
            messages.success(self.request, f'Added "{book.title}" to your {shelf_name} books.')
        elif status == 'to_read':
            user_shelf.to_read_books.add(book)
            messages.success(self.request, f'Added "{book.title}" to your {shelf_name} books.')


class BookList(ListView):
    model=Book
    context_object_name = 'book_list'


