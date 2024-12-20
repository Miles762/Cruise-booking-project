from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('ssh_cruise.urls')),  # Delegating to the app-level URLs
]
