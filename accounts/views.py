from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import OrganizerProfile
from events.models import Booking, Event


def register_attendee(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                first_name=first_name, last_name=last_name,
                password=password,
            )
            login(request, user)
            messages.success(request, f'Welcome, {first_name or username}!')
            return redirect('home')
    return render(request, 'accounts/register.html')


def register_organizer(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name   = request.POST.get('first_name', '').strip()
        last_name    = request.POST.get('last_name', '').strip()
        username     = request.POST.get('username', '').strip()
        email        = request.POST.get('email', '').strip()
        password     = request.POST.get('password', '')
        password2    = request.POST.get('password2', '')
        organization = request.POST.get('organization', '').strip()
        phone        = request.POST.get('phone', '').strip()

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                first_name=first_name, last_name=last_name,
                password=password,
            )
            OrganizerProfile.objects.create(
                user=user, organization=organization, phone=phone,
            )
            login(request, user)
            messages.success(request, f'Welcome, {first_name or username}! Start creating events.')
            return redirect('organizer_dashboard')
    return render(request, 'accounts/register_organizer.html')


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'organizer_profile'):
            return redirect('organizer_dashboard')
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'organizer_profile'):
                return redirect('organizer_dashboard')
            next_url = request.GET.get('next', '')
            return redirect(next_url if next_url else 'home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def attendee_dashboard(request):
    if hasattr(request.user, 'organizer_profile'):
        return redirect('organizer_dashboard')
    bookings = Booking.objects.filter(user=request.user).select_related('event').order_by('-booked_at')
    return render(request, 'accounts/dashboard.html', {'bookings': bookings})


@login_required
def organizer_dashboard(request):
    if not hasattr(request.user, 'organizer_profile'):
        return redirect('attendee_dashboard')
    events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    total_bookings = sum(e.bookings.filter(status='confirmed').count() for e in events)
    total_revenue  = sum(
        b.quantity * b.event.price
        for e in events
        for b in e.bookings.filter(status='confirmed')
    )
    ctx = {
        'events':         events,
        'total_bookings': total_bookings,
        'total_revenue':  total_revenue,
    }
    return render(request, 'accounts/organizer_dashboard.html', ctx)
