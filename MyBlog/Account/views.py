from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from Blog.models import Post, UserProfile
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserEditForm,
    ProfileImageForm,
    EmailChangeForm,
    CustomPasswordChangeForm,
)
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('Blog:blog_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Blog:blog_list')
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('Blog:blog_list')

@login_required
def profile(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    user_posts = Post.objects.filter(author=user)
    return render(request, 'account/profile.html', {'user': user, 'user_posts': user_posts})

@login_required
def edit_profile(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('Account:profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileImageForm(instance=user_profile)

    return render(request, 'account/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def account(request):
    return render(request, 'account/account.html')

login_required
def change_email(request):
    if request.method == 'POST':
        email_form = EmailChangeForm(instance=request.user, data=request.POST)
        if email_form.is_valid():
            user = email_form.save()
            update_session_auth_hash(request, user)  # Prevents logout after email change
            return redirect('Account:profile')
    else:
        email_form = EmailChangeForm(instance=request.user)
    
    return render(request, 'account/change_email.html', {'email_form': email_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            return redirect('Account:profile')
    else:
        password_form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'account/change_password.html', {'password_form': password_form})


@login_required
def settings(request):
    return render(request, 'account/settings.html')