
from django.urls import path
from .views import add_comment, add_reply, LikeCommentView
from ..books import views
from ..books.views import BookDetailView

urlpatterns = [

    path('<int:book_id>/add_comment/', add_comment, name='add_comment'),
    path('add_reply/<int:comment_id>/', add_reply, name='add_reply'),





]