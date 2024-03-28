from . import views
from django.urls import path
from .views import add_comment, like_comment, reply_comment

urlpatterns = [
    path('<int:book_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),


    # path('<int:comment_id>/like/', like_comment, name='like_comment'),
]