from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/register/',          api_views.RegisterAPIView.as_view(),        name='api-register'),
    path('auth/login/',             api_views.login_api,                        name='api-login'),
    path('events/',                 api_views.EventListAPIView.as_view(),        name='api-events'),
    path('events/<int:pk>/',        api_views.EventDetailAPIView.as_view(),      name='api-event-detail'),
    path('bookings/',               api_views.BookingListCreateAPIView.as_view(),name='api-bookings'),
    path('bookings/<int:pk>/cancel/', api_views.cancel_booking_api,             name='api-cancel-booking'),
]
