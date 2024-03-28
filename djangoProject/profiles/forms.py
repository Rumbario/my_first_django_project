from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from djangoProject.profiles.models import Profile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''

        if self['username'].value() or self.data.get('username'):

            self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

        self.fields['password1'].help_text = ''

        if self['password1'].value() or self.data.get('password1'):
            self.fields['password1'].error_messages = {
                'password_too_short': 'Your password must contain at least 8 characters.',
                'password_entirely_numeric': 'Your password can’t be entirely numeric.',
                'password_common': 'Your password can’t be a commonly used password.',
                'password_similar': 'Your password can’t be too similar to your other personal information.',

            }
        self.fields['password2'].help_text = ''
        if self['password2'].value() or self.data.get('password2'):
            self.fields['password2'].error_messages = {
                'password_mismatch': 'The two password fields didn’t match.',
            }


class UserSettingsForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.profile_picture = profile_picture
            profile.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


