from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import default
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Book, FavoriteBook, BookRating
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from django.views.generic import DetailView, ListView
from .models import Book
from django.contrib.auth.mixins import UserPassesTestMixin

from ..comments.forms import CommentForm, ReplyForm
from ..comments.models import Comment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        # Изчисляване на средния рейтинг
        average_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = average_rating

        all_comments = Comment.objects.filter(book=book)

        paginator = Paginator(all_comments, 4)
        page_number = self.request.GET.get('page')
        try:
            comments = paginator.page(page_number)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['reply_forms'] = {comment.id: ReplyForm() for comment in comments}
        context['pk'] = self.object.pk

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

        return context

    def post(self, request, *args, **kwargs):
        book_id = kwargs['pk']
        if request.method == 'POST':
            book = get_object_or_404(Book, pk=book_id)
            rating_field = request.POST.get('rating')
            rating = None
            if rating_field is not None:
                rating = int(rating_field.split('_')[-1])

            user = request.user

            if BookRating.objects.filter(user=user, book=book).exists():
                book_rating = BookRating.objects.get(user=user, book=book)
                book_rating.rating = rating
                book_rating.save()
            else:
                BookRating.objects.create(user=user, book=book, rating=rating)




        return redirect('book_detail', pk=book_id)


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


def add_to_favorites(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        FavoriteBook.objects.get_or_create(user=request.user, book=book)
        return redirect('favourites')

    return redirect('add_to_favorites', pk=pk)

def favourites_view(request):

    favorite_books = FavoriteBook.objects.filter(user=request.user)

    return render(request, 'books/favourites.html', {'favorite_books': favorite_books})


