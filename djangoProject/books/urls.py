from django.urls import path, include

from . import views
from .views import add_book, BookDeleteView, BookUpdateView, BookDetailView, add_to_favorites
from .views import GenreBooksListView
from djangoProject.comments.views import add_comment, add_reply,LikeCommentView


urlpatterns = [
    path('add_book/', add_book, name='add_book'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:book_id>/update/', BookUpdateView.as_view(), name='book_update'),
    path('genre/<str:genre>/', GenreBooksListView.as_view(), name='genre_books'),
    path('book/<int:book_id>/add_comment/', add_comment, name='add_comment'),
    path('add_reply/<int:comment_id>/', add_reply, name='add_reply'),
    path('books/<int:pk>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('books/like_comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),









]
