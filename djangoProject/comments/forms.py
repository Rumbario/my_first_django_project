from django import forms
from .models import ReplyComment

class CommentReplyForm(forms.ModelForm):
    text = forms.CharField(label='Отговор', widget=forms.Textarea(attrs={'rows': 3, 'cols': 50}))

    class Meta:
        model = ReplyComment
        fields = ['text']