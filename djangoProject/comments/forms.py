from django import forms
from .models import Comment, CommentReply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = False
        self.fields['text'].widget.attrs.update({'placeholder': 'Добави коментар...'})


    def set_user_data(self, user):
        self.fields['user'] = forms.CharField(initial=user.username, widget=forms.HiddenInput())
        self.fields['user_picture'] = forms.ImageField(initial=user.profile.picture.url, widget=forms.HiddenInput())

class ReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Отговори...'})
        }