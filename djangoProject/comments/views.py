
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Comment, CommentLike, ReplyComment
from ..books.models import Book
from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentReplyForm


@login_required
def add_comment(request, book_id):
    if request.method == 'POST':
        text = request.POST['text']
        book = get_object_or_404(Book, pk=book_id)
        Comment.objects.create(user=request.user, book=book, text=text)
        return redirect('book_detail', pk=book_id)
    else:
        return redirect('book_detail', pk=book_id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user
    if user.is_authenticated:
        if CommentLike.objects.filter(comment=comment, user=user).exists():

            CommentLike.objects.filter(comment=comment, user=user).delete()
        else:

            CommentLike.objects.create(comment=comment, user=user)
    return redirect('book_detail', book_id=comment.book.id)


@login_required
def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('book_detail', pk=comment.book.id)
    else:
        form = CommentReplyForm()

    replies = comment.replies.all()
    user_profile_picture = request.user.profile.profile_picture

    return render(request, 'books/book_detail.html', {'book': comment.book, 'replies': replies, 'form': form, 'user_profile_picture': user_profile_picture})


def redirect_to_latest_comment(request, book_id):
    latest_comment = Comment.objects.filter(book_id=book_id).latest('created_at')
    return redirect(reverse('book_detail', kwargs={'pk': latest_comment.book_id}) + f'#comment-{latest_comment.id}')




@login_required
def reply_to_reply(request, reply_id):
    reply = get_object_or_404(ReplyComment, id=reply_id)
    parent_comment = reply.comment

    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.comment = parent_comment
            new_reply.user = request.user
            new_reply.save()
            return redirect('book_detail', pk=parent_comment.book.id)
    else:
        form = CommentReplyForm()

    replies = parent_comment.replies.all()
    user_profile_picture = request.user.profile.profile_picture

    return render(request, 'books/book_detail.html', {'book': parent_comment.book, 'replies': replies, 'form': form, 'user_profile_picture': user_profile_picture})


