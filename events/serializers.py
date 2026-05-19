from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Category, Booking, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug']


class EventSerializer(serializers.ModelSerializer):
    category   = CategorySerializer(read_only=True)
    seats_left = serializers.SerializerMethodField()
    organizer  = serializers.StringRelatedField()

    class Meta:
        model  = Event
        fields = [
            'id', 'title', 'description', 'category', 'organizer',
            'venue', 'city', 'date', 'price', 'capacity',
            'seats_left', 'status', 'banner', 'created_at',
        ]

    def get_seats_left(self, obj):
        return obj.seats_left()


class BookingSerializer(serializers.ModelSerializer):
    event       = EventSerializer(read_only=True)
    event_id    = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.filter(status='published'), source='event', write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model  = Booking
        fields = ['id', 'event', 'event_id', 'quantity', 'status', 'booked_at', 'total_price']
        read_only_fields = ['status', 'booked_at']

    def get_total_price(self, obj):
        return obj.total_price()

    def validate(self, data):
        event    = data.get('event')
        quantity = data.get('quantity', 1)
        request  = self.context.get('request')

        if Booking.objects.filter(user=request.user, event=event, status='confirmed').exists():
            raise serializers.ValidationError('You have already booked this event.')
        if quantity > event.seats_left():
            raise serializers.ValidationError(f'Only {event.seats_left()} seats available.')
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'user', 'event', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
