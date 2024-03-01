from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import BookInventory

class BookInventory(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BookInventory
    success_url = reverse_lazy('bookshop:create_book')
    fields = ['book', 'price', 'quantity']
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
