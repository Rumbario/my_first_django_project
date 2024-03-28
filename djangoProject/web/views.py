from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render
from djangoProject.books.models import Book


class IndexView(View):
    template_name = 'web/index.html'
    items_per_page = 24

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.all()

        paginator = Paginator(book_list, self.items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = [
            'Българска литература',
            'Трилър',
            'Криминални романи',
            'Фантастика, Фентъзи, Хорър',
            'Биографична литература',
            'Техническа литература',
            'Образование',
            'Бизнес и икономика',
            'Здраве и диети',
            'Философска литература'
        ]

        category_counts = {category: Book.objects.filter(genre=category).count() for category in categories}

        return render(request, self.template_name, {'books': page_obj, 'categories': categories, 'category_counts': category_counts})
