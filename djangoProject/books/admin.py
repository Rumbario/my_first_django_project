from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'genre', 'pages', 'rating')
    list_filter = ('author', 'publication_year', 'genre')
    search_fields = ('title', 'author')

    readonly_fields = ('uploaded_by',)

admin.site.register(Book, BookAdmin)
