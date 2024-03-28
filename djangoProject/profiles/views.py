from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm, CustomPasswordChangeForm, UserSettingsForm
from .models import Profile


class UserLoginView(FormView):
    template_name = 'profiles/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

class UserRegisterView(FormView):
    template_name = 'profiles/register.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')





class UserSettingsView(View):
    def get(self, request, *args, **kwargs):
        form = UserSettingsForm(instance=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profiles/user_settings.html', {'form': form, 'profile': profile})

    def post(self, request, *args, **kwargs):
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.profile_picture = request.FILES.get('profile_picture')
            profile.save()
            messages.success(request, 'Your settings have been successfully updated.')
            return redirect('user_settings')
        return render(request, 'profiles/user_settings.html', {'form': form})







@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            return redirect('profiles/change_password.html')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'profiles/change_password.html', {'form': form})




