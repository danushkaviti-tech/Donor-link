from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import DonorRegistrationForm, DonorProfileForm, HospitalRegistrationForm
from .models import Donor, Hospital, DonationRequest  # Ensure DonationRequest is in models.py
from .filters import DonorFilter

# --- 1. SMART LOGIN ---
# This ensures hospitals go to dashboard and donors go to home
class CustomLoginView(LoginView):
    template_name = 'blood_app/login.html'

    def get_success_url(self):
        if hasattr(self.request.user, 'hospital'):
            return reverse_lazy('hospital_dashboard')
        return reverse_lazy('home')

# --- 2. NAVIGATION & AUTH ---
@login_required
def home(request):
    if hasattr(request.user, 'hospital'):
        return redirect('hospital_dashboard')
    return render(request, 'blood_app/donor_home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- 3. REGISTRATION ---
def register_donor(request):
    if request.method == 'POST':
        u_form = DonorRegistrationForm(request.POST)
        p_form = DonorProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.set_password(u_form.cleaned_data['password'])
            user.save()
            profile = p_form.save(commit=False)
            profile.user = user
            # Capture GPS from the hidden fields in your HTML
            profile.latitude = request.POST.get('user_lat')
            profile.longitude = request.POST.get('user_lon')
            profile.save()
            login(request, user)
            return redirect('home') 
    else:
        u_form = DonorRegistrationForm()
        p_form = DonorProfileForm()
    return render(request, 'blood_app/register.html', {'u_form': u_form, 'p_form': p_form, 'is_hospital': False})

def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Capture GPS for hospital
            Hospital.objects.create(
                user=user, 
                address=form.cleaned_data['address'],
                latitude=request.POST.get('user_lat'),
                longitude=request.POST.get('user_lon')
            )
            login(request, user)
            return redirect('hospital_dashboard')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'blood_app/register.html', {'form': form, 'is_hospital': True})

# --- 4. HOSPITAL DASHBOARD ---
@login_required
def hospital_dashboard(request):
    hospital = get_object_or_404(Hospital, user=request.user)
    donors = Donor.objects.filter(is_available=True)
    donor_filter = DonorFilter(request.GET, queryset=donors)
    
    final_donors = list(donor_filter.qs)
    for donor in final_donors:
        donor.distance = donor.get_distance_from(hospital.latitude, hospital.longitude)
    
    final_donors.sort(key=lambda x: x.distance)

    # NEW: Fetch the status of requests sent by this hospital
    recent_requests = DonationRequest.objects.filter(hospital=hospital).order_by('-created_at')

    return render(request, 'blood_app/dashboard.html', {
        'filter': donor_filter,
        'donors': final_donors,
        'recent_requests': recent_requests
    })

# --- 5. THE EMAIL YES/NO SYSTEM ---
@login_required
def send_request_email(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    hospital = request.user.hospital
    
    # Create the Request record in database to track the "Yes/No" click
    blood_req = DonationRequest.objects.create(hospital=hospital, donor=donor)
    
    base_url = f"http://{request.get_host()}"
    yes_url = f"{base_url}/respond/{blood_req.id}/yes/"
    no_url = f"{base_url}/respond/{blood_req.id}/no/"
    
    map_url = f"https://www.google.com/maps?q={hospital.latitude},{hospital.longitude}"
    
    send_mail(
        'URGENT: Blood Needed Nearby',
        f'Hello {donor.user.username},\n\nA hospital needs your help!\n'
        f'Location: {map_url}\n\n'
        f'Can you help save a life?\n'
        f'✅ YES, I am coming: {yes_url}\n'
        f'❌ NO, I cannot: {no_url}',
        'noreply@donorlink.com',
        [donor.user.email]
    )
    return redirect('hospital_dashboard')

def respond_to_request(request, request_id, decision):
    """View to handle the donor's click from the email (YES or NO)"""
    blood_req = get_object_or_404(DonationRequest, id=request_id)
    
    if decision == 'yes':
        blood_req.status = 'Accepted'
    else:
        blood_req.status = 'Rejected'
        
    blood_req.save()
    
    return render(request, 'blood_app/response_result.html', {
        'status': blood_req.status,
        'hospital': blood_req.hospital
    })