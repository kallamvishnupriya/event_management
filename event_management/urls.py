from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = 'Event Management Admin'
admin.site.site_title   = 'Event Management'
admin.site.index_title  = 'Dashboard'

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('accounts/',  include('accounts.urls')),
    path('',           include('events.urls')),
    path('api/',       include('events.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
