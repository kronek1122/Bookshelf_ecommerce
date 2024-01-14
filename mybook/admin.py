from django.contrib import admin

from .models import Genre, Author, Book, UserShelf, BookOpinion, Messages


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(UserShelf)
admin.site.register(BookOpinion)
admin.site.register(Messages)