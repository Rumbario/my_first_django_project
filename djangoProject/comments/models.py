from django.db import models
from django.contrib.auth.models import User
from djangoProject.books.models import Book


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} likes {self.comment}'


class CommentReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='replies', default=1)

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


