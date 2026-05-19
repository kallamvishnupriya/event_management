from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Event, Category, Booking, Review
from .serializers import (
    EventSerializer, CategorySerializer, BookingSerializer,
    ReviewSerializer, RegisterSerializer, UserSerializer,
)


# ── Auth ──────────────────────────────────────────────────────

class RegisterAPIView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user  = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Events ────────────────────────────────────────────────────

class EventListAPIView(generics.ListAPIView):
    serializer_class   = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs       = Event.objects.filter(status='published').select_related('category', 'organizer')
        query    = self.request.query_params.get('q')
        category = self.request.query_params.get('category')
        city     = self.request.query_params.get('city')
        if query:
            qs = qs.filter(title__icontains=query)
        if category:
            qs = qs.filter(category__slug=category)
        if city:
            qs = qs.filter(city__icontains=city)
        return qs


class EventDetailAPIView(generics.RetrieveAPIView):
    queryset           = Event.objects.filter(status='published')
    serializer_class   = EventSerializer
    permission_classes = [permissions.AllowAny]


# ── Bookings ──────────────────────────────────────────────────

class BookingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('event')


@api_view(['PUT'])
def cancel_booking_api(request, pk):
    try:
        booking = Booking.objects.get(pk=pk, user=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
    booking.status = 'cancelled'
    booking.save()
    return Response({'message': 'Booking cancelled.'})
