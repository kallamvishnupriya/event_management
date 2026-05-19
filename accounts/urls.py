from django.urls import path
from . import views

urlpatterns = [
    path('register/',             views.register_attendee,   name='register'),
    path('register/organizer/',   views.register_organizer,  name='register_organizer'),
    path('login/',                views.login_view,           name='login'),
    path('logout/',               views.logout_view,          name='logout'),
    path('dashboard/',            views.attendee_dashboard,   name='attendee_dashboard'),
    path('organizer/dashboard/',  views.organizer_dashboard,  name='organizer_dashboard'),
]
