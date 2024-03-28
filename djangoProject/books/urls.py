from django.urls import path, include
from .views import add_book, BookDeleteView, BookUpdateView, BookDetailView
from .views import GenreBooksListView
from djangoProject.comments.views import add_comment, redirect_to_latest_comment
from djangoProject.comments.views import reply_comment



urlpatterns = [
    path('add_book/', add_book, name='add_book'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:book_id>/update/', BookUpdateView.as_view(), name='book_update'),
    path('genre/<str:genre>/', GenreBooksListView.as_view(), name='genre_books'),
    path('book/<int:book_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),

]
