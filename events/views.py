from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Event, Category, Booking, Review
from accounts.decorators import organizer_required, attendee_required


# ── Public Views ──────────────────────────────────────────────

def home(request):
    events     = Event.objects.filter(status='published').select_related('category', 'organizer')
    categories = Category.objects.all()
    query      = request.GET.get('q', '')
    category   = request.GET.get('category', '')
    city       = request.GET.get('city', '')

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        events = events.filter(category__slug=category)
    if city:
        events = events.filter(city__icontains=city)

    paginator = Paginator(events, 9)
    page      = paginator.get_page(request.GET.get('page'))

    ctx = {
        'page_obj':   page,
        'categories': categories,
        'query':      query,
        'selected_category': category,
        'selected_city':     city,
    }
    return render(request, 'events/home.html', ctx)


def event_detail(request, pk):
    event   = get_object_or_404(Event, pk=pk, status='published')
    reviews = event.reviews.select_related('user')
    user_booked  = False
    user_reviewed = False

    if request.user.is_authenticated:
        user_booked   = Booking.objects.filter(user=request.user, event=event, status='confirmed').exists()
        user_reviewed = Review.objects.filter(user=request.user, event=event).exists()

    ctx = {
        'event':        event,
        'reviews':      reviews,
        'user_booked':  user_booked,
        'user_reviewed': user_reviewed,
    }
    return render(request, 'events/event_detail.html', ctx)


# ── Organizer Views ───────────────────────────────────────────

@organizer_required
def event_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        venue       = request.POST.get('venue', '').strip()
        city        = request.POST.get('city', '').strip()
        date        = request.POST.get('date')
        price       = request.POST.get('price', 0)
        capacity    = request.POST.get('capacity', 100)
        banner      = request.FILES.get('banner')
        status      = request.POST.get('status', 'published')

        if not all([title, description, venue, city, date]):
            messages.error(request, 'Please fill all required fields.')
        else:
            event = Event.objects.create(
                organizer   = request.user,
                category_id = category_id or None,
                title       = title,
                description = description,
                venue       = venue,
                city        = city,
                date        = date,
                price       = price,
                capacity    = capacity,
                banner      = banner,
                status      = status,
            )
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_form.html', {'categories': categories, 'action': 'Create'})


@organizer_required
def event_edit(request, pk):
    event      = get_object_or_404(Event, pk=pk, organizer=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        event.title       = request.POST.get('title', '').strip()
        event.description = request.POST.get('description', '').strip()
        event.category_id = request.POST.get('category') or None
        event.venue       = request.POST.get('venue', '').strip()
        event.city        = request.POST.get('city', '').strip()
        event.date        = request.POST.get('date')
        event.price       = request.POST.get('price', 0)
        event.capacity    = request.POST.get('capacity', 100)
        event.status      = request.POST.get('status', 'published')
        if request.FILES.get('banner'):
            event.banner  = request.FILES['banner']
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_form.html', {
        'categories': categories, 'event': event, 'action': 'Edit'
    })


@organizer_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('organizer_dashboard')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


@organizer_required
def event_bookings(request, pk):
    event    = get_object_or_404(Event, pk=pk, organizer=request.user)
    bookings = event.bookings.filter(status='confirmed').select_related('user')
    total_revenue = sum(b.total_price() for b in bookings)
    ctx = {
        'event':         event,
        'bookings':      bookings,
        'total_revenue': total_revenue,
    }
    return render(request, 'events/event_bookings.html', ctx)


# ── Attendee Views ────────────────────────────────────────────

@attendee_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk, status='published')

    if Booking.objects.filter(user=request.user, event=event, status='confirmed').exists():
        messages.info(request, 'You have already booked this event.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
        elif quantity > event.seats_left():
            messages.error(request, f'Only {event.seats_left()} seats left.')
        else:
            Booking.objects.create(user=request.user, event=event, quantity=quantity)
            messages.success(request, f'Successfully booked {quantity} ticket(s) for {event.title}!')
            return redirect('attendee_dashboard')

    return render(request, 'events/book_event.html', {'event': event})


@attendee_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('attendee_dashboard')
    return render(request, 'events/cancel_booking.html', {'booking': booking})


@attendee_required
def write_review(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if not Booking.objects.filter(user=request.user, event=event, status='confirmed').exists():
        messages.error(request, 'You can only review events you have booked.')
        return redirect('event_detail', pk=pk)

    if Review.objects.filter(user=request.user, event=event).exists():
        messages.info(request, 'You have already reviewed this event.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        rating  = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if not rating:
            messages.error(request, 'Please select a rating.')
        else:
            Review.objects.create(user=request.user, event=event, rating=rating, comment=comment)
            messages.success(request, 'Review submitted!')
            return redirect('event_detail', pk=pk)

    return render(request, 'events/review_form.html', {'event': event})
