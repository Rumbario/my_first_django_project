from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from .forms import CommentForm, ReplyForm
from .models import Comment, CommentLike, CommentReply
from ..books.models import Book

@login_required
def add_comment(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = Comment.objects.create(user=request.user, book=book, text=text)
            redirect_url = reverse('book_detail', kwargs={'pk': book_id}) + f'?comment_id={comment.pk}'
            return HttpResponseRedirect(redirect_url)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(book=book)
    return render(request, 'books/book_detail.html', {'form': form, 'comments': comments, 'book': book})


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data['text']
            reply = CommentReply.objects.create(user=request.user, comment=comment, text=reply_text)
            return redirect('book_detail', pk=comment.book.pk)
    else:
        form = ReplyForm()
    return render(request, 'books/book_detail.html', {'form': form, 'comment': comment})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = Comment.objects.filter(book=book).order_by('-created_at')
    comment_replies = CommentReply.objects.filter(comment__in=comments).select_related('comment').order_by('-created_at')
    comment_reply_dict = {}
    for reply in comment_replies:
        if reply.comment_id not in comment_reply_dict:
            comment_reply_dict[reply.comment_id] = []
        comment_reply_dict[reply.comment_id].append(reply)
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        if comment_id:
            return LikeCommentView.as_view()(request, comment_id=comment_id)
    return render(request, 'books/book_detail.html', {'book': book, 'comments': comments, 'comment_replies': comment_reply_dict})


class LikeCommentView(View):
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        user_id = request.user.id
        if user_id:
            if not CommentLike.objects.filter(comment_id=comment_id, user_id=user_id).exists():

                CommentLike.objects.create(comment_id=comment_id, user_id=user_id)



        return redirect('book_detail', book_id=comment.book.id)
