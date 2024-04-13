from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'publication_year', 'genre', 'pages', 'calculate_average_rating')


    list_filter = ('author', 'genre', 'publication_year')


    search_fields = ['title', 'author']


    ordering = ('title',)


    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'genre', 'pages', 'description', 'uploaded_by', 'book_cover')
        }),
    )





admin.site.register(Book, BookAdmin)

