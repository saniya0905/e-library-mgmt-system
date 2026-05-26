from django.contrib import admin
from .models import UserProfile, Category, Book, Bookmark

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Bookmark)