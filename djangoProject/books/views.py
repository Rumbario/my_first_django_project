from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from django.views.generic import DetailView, ListView
from .models import Book
from django.contrib.auth.mixins import UserPassesTestMixin

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})




class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('index')



@method_decorator(login_required, name='dispatch')
class BookUpdateView(View):
    template_name = 'books/book_update.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        form = BookForm(instance=book)
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form, 'book': book})


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_superuser_or_staff'] = self.request.user.is_superuser or self.request.user.is_staff


        comment_id = self.request.GET.get('comment_id')
        comment = None
        context['comment'] = comment


        book_id = self.object.id
        context['book_id'] = book_id

        return context



class GenreBooksListView(ListView):
    model = Book
    template_name = 'books/genre_books.html'
    context_object_name = 'books'
    paginate_by = 24

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.kwargs['genre']
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
        context['categories'] = categories
        context['category_counts'] = category_counts
        context['genre'] = genre
        return context