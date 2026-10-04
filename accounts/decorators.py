from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def teacher_required(view_func):
    """Allow only authenticated users with role='teacher'."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # Only wrap the profile lookup in try/except — NOT the view call
        try:
            profile = request.user.profile
        except Exception:
            messages.error(request, 'Profile not found. Please log in again.')
            return redirect('login')

        if profile.role == 'teacher':
            return view_func(request, *args, **kwargs)  # Any exception here will propagate normally

        messages.error(request, 'Access denied: this area is for teachers only.')
        return redirect('student_dashboard')

    return wrapper


def student_required(view_func):
    """Allow only authenticated users with role='student'."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            profile = request.user.profile
        except Exception:
            messages.error(request, 'Profile not found. Please log in again.')
            return redirect('login')

        if profile.role == 'student':
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Access denied: this area is for students only.')
        return redirect('teacher_dashboard')

    return wrapper
