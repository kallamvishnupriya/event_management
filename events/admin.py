from django.contrib import admin
from .models import Category, Event, Booking, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display   = ['title', 'organizer', 'category', 'city', 'date', 'price', 'capacity', 'status']
    list_filter    = ['status', 'category', 'city']
    search_fields  = ['title', 'organizer__username', 'city']
    list_editable  = ['status']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['user', 'event', 'quantity', 'status', 'booked_at']
    list_filter   = ['status']
    search_fields = ['user__username', 'event__title']
    list_editable = ['status']
    readonly_fields = ['booked_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['user', 'event', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['created_at']
