from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'mybook/home.html')


@login_required
def user_view(request):
    return render(request, 'mybook/user_view.html')