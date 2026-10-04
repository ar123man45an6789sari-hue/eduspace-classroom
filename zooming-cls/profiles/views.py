from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}! 🎉 Account created.")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = user.profile

    # Classrooms depending on role
    if profile.is_teacher:
        classrooms = user.taught_classrooms.filter(is_active=True)
    else:
        classrooms = user.enrolled_classrooms.filter(is_active=True)

    return render(request, 'profiles/profile.html', {
        'profile_user': user,
        'profile': profile,
        'classrooms': classrooms,
        'is_own_profile': user == request.user,
    })


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profiles/profile_edit.html', {'form': form})
