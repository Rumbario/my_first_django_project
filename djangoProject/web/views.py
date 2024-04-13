from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View
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

    def post(self, request, *args, **kwargs):
        query = request.POST.get('search_authenticated')
        if not query:
            query = request.POST.get('search_anonymous')

        if query:
            results = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)

            if results:
                request.session['search_result'] = [result.id for result in results]
                return redirect('index', query=query)
            else:
                return render(request, self.template_name, {'message': 'Няма намерени резултати'})


