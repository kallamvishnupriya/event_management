from django.db import models
from django.contrib.auth.models import User


class OrganizerProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer_profile')
    organization    = models.CharField(max_length=200, blank=True)
    phone           = models.CharField(max_length=15, blank=True)
    bio             = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Organizer: {self.user.username}'
