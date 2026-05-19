from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ]

    organizer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='events')
    title       = models.CharField(max_length=200)
    description = models.TextField()
    venue       = models.CharField(max_length=300)
    city        = models.CharField(max_length=100)
    date        = models.DateTimeField()
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity    = models.PositiveIntegerField(default=100)
    banner      = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def seats_left(self):
        booked = self.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        return self.capacity - booked

    def is_available(self):
        return self.seats_left() > 0 and self.status == 'published'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event     = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    quantity  = models.PositiveIntegerField(default=1)
    status    = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} → {self.event.title}'

    def total_price(self):
        return self.quantity * self.event.price


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    event      = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.IntegerField(choices=RATING_CHOICES)
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} → {self.event.title} ({self.rating}★)'
