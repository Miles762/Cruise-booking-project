from django.urls import path
from . import views

urlpatterns = [
    
    path('booking/', views.booking, name='booking'),
    path('process-booking/', views.process_booking, name='process_booking'),
    path('invoice/', views.invoice, name='invoice'),
    path('payment/', views.payment, name='payment'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path("success/", views.success, name="success"),
    path('analysis/', views.passenger_analysis, name='passenger_analysis'),
]
