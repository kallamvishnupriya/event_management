from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.home,            name='home'),
    path('events/<int:pk>/',            views.event_detail,    name='event_detail'),
    path('events/create/',              views.event_create,    name='event_create'),
    path('events/<int:pk>/edit/',       views.event_edit,      name='event_edit'),
    path('events/<int:pk>/delete/',     views.event_delete,    name='event_delete'),
    path('events/<int:pk>/book/',       views.book_event,      name='book_event'),
    path('events/<int:pk>/bookings/',   views.event_bookings,  name='event_bookings'),
    path('events/<int:pk>/review/',     views.write_review,    name='write_review'),
    path('bookings/<int:pk>/cancel/',   views.cancel_booking,  name='cancel_booking'),
]
