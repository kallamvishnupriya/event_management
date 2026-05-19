from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Category, Event
from accounts.models import OrganizerProfile


class Command(BaseCommand):
    help = 'Seed database with sample categories and events'

    def handle(self, *args, **kwargs):
        # Categories
        categories_data = [
            ('Music', 'music'),
            ('Technology', 'technology'),
            ('Sports', 'sports'),
            ('Food & Drink', 'food-drink'),
            ('Arts', 'arts'),
            ('Business', 'business'),
        ]
        categories = {}
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, slug=slug)
            categories[slug] = cat
        self.stdout.write('✅ Categories created')

        # Organizer user
        if not User.objects.filter(username='organizer1').exists():
            org_user = User.objects.create_user(
                username='organizer1', email='organizer@example.com',
                first_name='Event', last_name='Organizer',
                password='organizer123',
            )
            OrganizerProfile.objects.create(user=org_user, organization='EventHub Co.', phone='9999999999')
            self.stdout.write('✅ Organizer user created (username: organizer1, password: organizer123)')
        else:
            org_user = User.objects.get(username='organizer1')

        # Attendee user
        if not User.objects.filter(username='attendee1').exists():
            User.objects.create_user(
                username='attendee1', email='attendee@example.com',
                first_name='John', last_name='Doe',
                password='attendee123',
            )
            self.stdout.write('✅ Attendee user created (username: attendee1, password: attendee123)')

        # Sample events
        events_data = [
            {
                'title': 'Rock Music Night',
                'description': 'An electrifying night of live rock music featuring top local bands. Experience the energy of live performance at its finest.',
                'category': 'music',
                'venue': 'City Amphitheatre',
                'city': 'Hyderabad',
                'price': 500,
                'capacity': 200,
                'days': 7,
            },
            {
                'title': 'Python & Django Workshop',
                'description': 'A hands-on workshop covering Python basics, Django framework, REST APIs and deployment. Perfect for beginners and intermediate developers.',
                'category': 'technology',
                'venue': 'Tech Hub',
                'city': 'Bangalore',
                'price': 999,
                'capacity': 50,
                'days': 14,
            },
            {
                'title': 'Startup Pitch Night',
                'description': 'Watch 10 exciting startups pitch their ideas to investors. Network with founders, investors and industry leaders.',
                'category': 'business',
                'venue': 'Innovation Centre',
                'city': 'Mumbai',
                'price': 0,
                'capacity': 150,
                'days': 10,
            },
            {
                'title': 'Food Festival 2025',
                'description': 'Celebrate the diversity of Indian cuisine with 50+ food stalls, live cooking demos, and celebrity chefs.',
                'category': 'food-drink',
                'venue': 'Central Park',
                'city': 'Delhi',
                'price': 200,
                'capacity': 500,
                'days': 5,
            },
            {
                'title': 'Marathon Run 2025',
                'description': 'Join thousands of runners for our annual marathon. Categories: 5K, 10K, and Full Marathon. All fitness levels welcome.',
                'category': 'sports',
                'venue': 'City Stadium',
                'city': 'Chennai',
                'price': 300,
                'capacity': 1000,
                'days': 20,
            },
            {
                'title': 'Photography Exhibition',
                'description': 'A stunning collection of photographs from renowned artists across India. Explore themes of nature, culture and urban life.',
                'category': 'arts',
                'venue': 'Art Gallery',
                'city': 'Hyderabad',
                'price': 100,
                'capacity': 80,
                'days': 3,
            },
        ]

        for data in events_data:
            if not Event.objects.filter(title=data['title']).exists():
                Event.objects.create(
                    organizer   = org_user,
                    category    = categories[data['category']],
                    title       = data['title'],
                    description = data['description'],
                    venue       = data['venue'],
                    city        = data['city'],
                    date        = timezone.now() + timedelta(days=data['days']),
                    price       = data['price'],
                    capacity    = data['capacity'],
                    status      = 'published',
                )
        self.stdout.write('✅ Sample events created')
        self.stdout.write(self.style.SUCCESS('\n🎉 Seed data loaded successfully!'))
        self.stdout.write('   Organizer → username: organizer1  password: organizer123')
        self.stdout.write('   Attendee  → username: attendee1   password: attendee123')
