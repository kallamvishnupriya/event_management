from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def organizer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'organizer_profile'):
            messages.error(request, 'You must be an organizer to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def attendee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'organizer_profile'):
            messages.error(request, 'Organizers cannot perform this action.')
            return redirect('organizer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
