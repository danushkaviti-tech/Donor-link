from django.urls import path
from . import views

urlpatterns = [
    # Navigation & Home
    path('', views.home, name='home'),
    
    # Registration
    path('register/donor/', views.register_donor, name='register_donor'),
    path('register/hospital/', views.register_hospital, name='register_hospital'),
    
    # Authentication (Using our CustomLoginView for smart redirecting)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'), 
    
    # Hospital Portal
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    
    # Email Triggering
    path('send-email/<int:donor_id>/', views.send_request_email, name='send_request_email'),
    
    # The "Smart" Response URL (Handles both Yes and No clicks from Email)
    path('respond/<int:request_id>/<str:decision>/', views.respond_to_request, name='respond_to_request'),
]