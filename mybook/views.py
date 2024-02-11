from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseServerError, Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Count, Avg, Q

from statistics import mean
from datetime import datetime

from .forms import UserDataChangeForm, UsernameChangeForm, PostForm
from .models import Book, UserShelf, BookOpinion, UserFollow, Post, Author, Genre
from bookshop.models import BookInventory, UserShoppingCart
from .utils import get_book_cover_info


def home(request):
    books = Book.objects.all()
    book_opinions = BookOpinion.objects.all()
    
    read_books_this_month = book_opinions.filter(read_date__month=datetime.now().month, read_date__year=datetime.now().year)
    read_books_this_year = book_opinions.filter(read_date__year=datetime.now().year)
    most_read = Book.objects.annotate(total_read=Count('bookopinion__read_date')).order_by('-total_read').first()
    if most_read is not None and most_read.total_read > 0:
        pass
    else:
        most_read = None
    best_rating = Book.objects.annotate(avg_rating=Avg('bookopinion__rating')).filter(~Q(avg_rating=None)).order_by('-avg_rating').first()

    contex = {
        'books': books,
        'book_opinions' : book_opinions,
        'read_books_this_month' : read_books_this_month,
        'read_books_this_year' : read_books_this_year,
        'most_read' : most_read,
        'best_rating' : best_rating,
    }
    return render(request, 'mybook/home.html', contex)


@login_required
def user_view(request):

    user_shelf = None
    user_opinions = []
    read_books = []
    to_read_books = []
    read_books_this_month = []
    read_books_this_year = []
    user_follow_list = None
    followers_list = []
    following_list = []

    try:
        user_shelf = UserShelf.objects.get(user=request.user)
        user_opinions = BookOpinion.objects.filter(shelf=user_shelf)
        read_books = user_shelf.read_books.all()
        to_read_books = user_shelf.to_read_books.all()
        read_books_this_month = user_opinions.filter(read_date__month=datetime.now().month, read_date__year=datetime.now().year)
        read_books_this_year = user_opinions.filter(read_date__year=datetime.now().year)
    
    except UserShelf.DoesNotExist:
        user_shelf = None
        read_books = to_read_books = read_books_this_month = read_books_this_year = []

    try:
        user_follow_list = UserFollow.objects.get(user=request.user)
        followers_list = user_follow_list.following.all()
        following_list = user_follow_list.followers.all()
    
    except UserFollow.DoesNotExist:
        user_follow_list = None
        followers_list = following_list = []

    context = {
        'user_shelf': user_shelf,
        'read_books': read_books,
        'to_read_books': to_read_books,
        'user_opinions': user_opinions,
        'read_books_this_month': read_books_this_month,
        'read_books_this_year': read_books_this_year,
        'user_follow_list': user_follow_list,
        'followers_list': followers_list,
        'following_list': following_list,
}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'remove_book':
            book_id = request.POST.get('book_id')
            try:
                user_shelf = UserShelf.objects.get(user=request.user)
                user_shelf.read_books.remove(book_id)
                BookOpinion.objects.filter(shelf=user_shelf, book_id=book_id).delete()
            except UserShelf.DoesNotExist:
                pass

        elif action == 'remove_to_read_book':
            book_id = request.POST.get('book_id')
            user_shelf.to_read_books.remove(book_id)

        elif action == 'delete_opinion':
            opinion_id = request.POST.get('opinion_id')
            try:
                user_shelf = UserShelf.objects.get(user=request.user)
                BookOpinion.objects.filter(shelf=user_shelf, id=opinion_id).delete()
            except UserShelf.DoesNotExist:
                pass

        elif action == 'edit_book':
            book_id = request.POST.get('book_id')

            try:
                read_book = BookOpinion.objects.get(
                    book=book_id,
                    shelf=user_shelf,
                )
            except BookOpinion.DoesNotExist: 
                book = Book.objects.get(pk=book_id)
                read_book, created = BookOpinion.objects.get_or_create(
                    book=book,
                    shelf=user_shelf,
                    defaults={'read_date': timezone.now().date(), 'review': '', 'rating': None}

                )

            review = request.POST.get('review')
            rating = request.POST.get('rating')
            read_date = request.POST.get('read_date')

            if review:
                read_book.review = review

            if rating:
                read_book.rating = int(rating)

            if read_date:
                read_book.read_date = read_date

            read_book.save()

        return HttpResponseRedirect(request.path)

    return render(request, 'mybook/profile.html', context)


class AnotherUserView(View):

    def get(self, request, username=None):

        if request.user.username == username:
            return redirect('mybook:profile')
        try:
            is_following = False
            current_user = UserFollow.objects.get(user=self.request.user)

            for following_user in current_user.following.all():
                if following_user.username == username:
                    is_following = True
                    break

        except UserFollow.DoesNotExist:
            is_following = False

        try:
            if username:
                user = User.objects.get(username=username)
                user_shelf = UserShelf.objects.get(user=user)
                user_opinions = BookOpinion.objects.filter(shelf=user_shelf)

                read_books = user_shelf.read_books.all()
                to_read_books = user_shelf.to_read_books.all()
                read_books_this_month = user_opinions.filter(
                    read_date__month=datetime.now().month, 
                    read_date__year=datetime.now().year
                    )
                read_books_this_year = user_opinions.filter(
                    read_date__year=datetime.now().year
                    )

                context = {
                    'read_books': read_books,
                    'to_read_books': to_read_books,
                    'user_opinions' : user_opinions,
                    'read_books_this_month' : read_books_this_month,
                    'read_books_this_year' : read_books_this_year,
                    'user_profile' : user,
                    'is_following': is_following,
                }
            else:
                return HttpResponseServerError("Invalid username.")
    
        except User.DoesNotExist:
            raise Http404("User does not exist.")
        
        except UserShelf.DoesNotExist:
            context = {
                'read_books': '',
                'to_read_books': '',
                'user_profile' : user,
                'is_following': is_following,
            }

        return render(request, 'mybook/another_user_view.html', context)
    
    def post(self, request, username=None):
        action = request.POST.get('action')
        username_id = request.POST.get('username')
        username = User.objects.get(pk=username_id)

        if action == 'follow':
            self.manage_follow_status('follow', username=username)
        elif action == 'unfollow':
            self.manage_follow_status('unfollow',username=username)
        else:
            messages.warning(request, 'Invalid action.')

        return redirect('mybook:another_user_profile', username=self.kwargs['username'])

    def manage_follow_status(self, status, username):
        current_user_follow_list, created = UserFollow.objects.get_or_create(user=self.request.user)
        target_user_follow_list, created = UserFollow.objects.get_or_create(user=username)

        if status == 'follow':
            current_user_follow_list.following.add(username)
            target_user_follow_list.followers.add(self.request.user)
            messages.success(self.request, f'Now, you follow {username}.')

        elif status == 'unfollow':
            current_user_follow_list.following.remove(username)
            target_user_follow_list.followers.remove(self.request.user)
            messages.success(self.request, f'{username} unfollowed.')


@login_required
def delete_user(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')

        if confirmation.lower() == request.user.username.lower():
            request.user.delete()
            messages.success(request, 'Your account has been successfully deleted')
            return redirect('home')

        else:
            messages.error(request, 'Invalid confirmation. Your account was not deleted')
            
    
    return render(request, 'mybook/delete_user.html')


@login_required
def user_settings(request):
    return render(request, 'mybook/setting_page.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'mybook/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been successfully registered')
        return response


class BookCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    success_url = reverse_lazy('mybook:create_book')
    fields = ['title', 'author', 'isbn', 'genre', 'description']
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class BookDetail(DetailView):
    model=Book
    context_object_name = 'book_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs['pk'])

        context['genres'] = book.genre.all()
        context['opinions'] = book.get_opinions()

        ratings = [opinion.rating for opinion in context['opinions'] if opinion.rating is not None]
        context['average_rating'] = round(mean(ratings), 1) if ratings else None

        cover_info = get_book_cover_info(book.isbn)
        context['cover_url'] = cover_info['large'] if cover_info else None

        context['description'] = book.description

        context['book_inventory'] = BookInventory.objects.get(book=book)

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'add_to_read':
            self.add_book_to_shelf('read', 'Read')
        elif action == 'add_to_to_read':
            self.add_book_to_shelf('to_read', 'To Read')
        elif action == 'add_to_shopping_cart':
            self.add_book_to_shopping_cart() 
        else:
            messages.warning(request, 'Invalid action.')

        return redirect('mybook:book_detail', pk=self.kwargs['pk'])

    def add_book_to_shelf(self, status, shelf_name):
        book = self.get_object()
        user_shelf, created = UserShelf.objects.get_or_create(user=self.request.user)

        if status == 'read':
            user_shelf.read_books.add(book)

            read_book, created = BookOpinion.objects.get_or_create(
                book=book,
                shelf=user_shelf,
                defaults={'read_date': timezone.now().date(), 'review': '', 'rating': None}
            )

            review = self.request.POST.get('review')
            rating = self.request.POST.get('rating')
            read_date = self.request.POST.get('read_date')

            if review:
                read_book.review = review

            if rating:
                read_book.rating = int(rating)

            if read_date:
                read_book.read_date = read_date

            read_book.save()

            if not created:
                messages.warning(self.request, f'You have already marked "{book.title}" as read.')
            else:
                messages.success(self.request, f'Added "{book.title}" to your {shelf_name} books.')

        elif status == 'to_read':
            user_shelf.to_read_books.add(book)
            messages.success(self.request, f'Added "{book.title}" to your {shelf_name} books.')
        
    def add_book_to_shopping_cart(self):
        book = self.get_object()
        purchased_book = BookInventory.objects.get(book=book)
        user_shopping_cart, created = UserShoppingCart.objects.get_or_create(user=self.request.user)

        user_shopping_cart.books_to_buy.add(purchased_book)
        messages.success(self.request, f'Added "{book.title}" to your shopping cart')
        

class BookList(ListView):
    model=Book
    context_object_name = 'book_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()

        sort_by = self.request.GET.get('sort_by', 'title')
        filter_field = self.request.GET.get('filter_field')
        filter_value = self.request.GET.get('filter_value')

        if sort_by in [field.name for field in Book._meta.get_fields()]:
            queryset = queryset.order_by(sort_by)

        if filter_field and filter_value:
            filter_args = {f"{filter_field}__icontains": filter_value}
            queryset = queryset.filter(**filter_args)

        return queryset


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm


class UserDataChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserDataChangeForm
    template_name = 'registration/user_data_change_form.html'
    success_url = reverse_lazy('mybook:change_user_data_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserDataChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/user_data_change_done.html'


class UsernameChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UsernameChangeForm
    template_name = 'registration/username_change_form.html'
    success_url = reverse_lazy('mybook:change_username_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UsernameChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/username_change_done.html'


def search_bar(request):
    query = request.GET.get('query')
    book_result = Book.objects.filter(title__icontains=query)
    author_result = Book.objects.filter(author__last_name__icontains=query)
    genre_result = Book.objects.filter(genre__name__icontains=query)
    
    results_books = list(set(book_result) | set(author_result) | set(genre_result))
    results_users = User.objects.filter(username__icontains=query)

    return render(request, 'mybook/search_result.html', {'results_books':results_books,'results_users':results_users, 'query':query})


@login_required
def user_inbox(request):
    return render(request, 'postman/inbox.html')


class FollowList(LoginRequiredMixin,ListView):
    model=UserFollow
    template_name = 'mybook/follow_list.html'
    context_object_name = 'user_list'

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = UserFollow.objects.get(user=self.request.user)
        
        except UserFollow.DoesNotExist:
            queryset = None

        return queryset
    

def board(request):
    posts = Post.objects.order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_post':
            form = PostForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return redirect('mybook:board')
        elif action == 'delete_post':
            post_id = request.POST.get('post_id')
            try:
                Post.objects.filter(user=request.user, id=post_id).delete()
            except Post.DoesNotExist:
                pass
        return HttpResponseRedirect(request.path)

    else:
        form = PostForm()

    return render(request, 'mybook/board.html', {'posts': posts, 'form': form})    


class AuthorCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Author
    success_url = reverse_lazy('mybook:create_author')
    fields = ['first_name', 'last_name']
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class GenreCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Genre
    success_url = reverse_lazy('mybook:create_genre')
    fields = ['name']
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff