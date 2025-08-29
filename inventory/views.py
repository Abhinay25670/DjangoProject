from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, F
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.http import Http404
from datetime import timedelta
import os
from .models import Medicine, UserProfile
from .forms import UserRegistrationForm, MedicineForm
from .reports import MedicineReportGenerator
from django.conf import settings

def get_or_create_user_profile(user):
    """Get or create UserProfile for a user"""
    try:
        return user.userprofile
    except UserProfile.DoesNotExist:
        # Create UserProfile if it doesn't exist (safety measure)
        return UserProfile.objects.create(user=user, email_verified=True)

def send_verification_email(user):
    """Send verification email to user"""
    subject = 'Verify your PharmaTrack account'
    
    # Create verification URL
    verification_url = reverse('verify_email', kwargs={'token': user.userprofile.email_verification_token})
    
    # Get the base URL from settings or use the request domain
    base_url = getattr(settings, 'BASE_URL', 'https://your-app-name.railway.app')
    if not base_url or base_url == 'https://your-app-name.railway.app':
        # Try to get from environment variable
        base_url = os.environ.get('BASE_URL', 'https://your-app-name.railway.app')
    
    full_url = f"{base_url}{verification_url}"
    
    # Render email template
    html_message = render_to_string('inventory/email/verification_email.html', {
        'user': user,
        'verification_url': full_url,
    })
    plain_message = strip_tags(html_message)
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    # Update sent timestamp
    user.userprofile.email_verification_sent_at = timezone.now()
    user.userprofile.save()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't log them in yet
            user = form.save(commit=False)
            user.is_active = False  # User must verify email before being active
            user.save()
            
            # Send verification email
            try:
                send_verification_email(user)
                messages.success(request, 'Account created successfully! Please check your email to verify your account before logging in.')
                return redirect('login')
            except Exception as e:
                # Log the error for debugging
                print(f"Email sending failed: {str(e)}")
                # If email fails, delete the user and show error
                user.delete()
                messages.error(request, f'Failed to send verification email: {str(e)}. Please check your email configuration or contact support.')
                return render(request, 'inventory/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'inventory/register.html', {'form': form})

def verify_email(request, token):
    """Verify user email with token"""
    try:
        profile = UserProfile.objects.get(email_verification_token=token)
        
        # Check if token is expired (24 hours)
        if profile.email_verification_sent_at:
            time_diff = timezone.now() - profile.email_verification_sent_at
            if time_diff > timedelta(hours=settings.EMAIL_VERIFICATION_TIMEOUT_HOURS):
                messages.error(request, 'Verification link has expired. Please request a new one.')
                return redirect('resend_verification')
        
        # Mark email as verified and activate user
        profile.email_verified = True
        profile.save()
        
        user = profile.user
        user.is_active = True
        user.save()
        
        messages.success(request, 'Email verified successfully! You can now log in to your account.')
        return redirect('login')
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')

def resend_verification(request):
    """Resend verification email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile = get_or_create_user_profile(user)
            if not profile.email_verified:
                # Generate new token
                profile.email_verification_token = UserProfile._meta.get_field('email_verification_token').default()
                profile.save()
                
                # Send new verification email
                send_verification_email(user)
                messages.success(request, 'Verification email sent successfully! Please check your inbox.')
            else:
                messages.info(request, 'This email is already verified. You can log in.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
    
    return render(request, 'inventory/resend_verification.html')

def logout_view(request):
    """Custom logout view that ensures complete session cleanup"""
    # Always logout regardless of authentication status for security
    if request.user.is_authenticated:
        # Clear any session data
        request.session.flush()
        # Logout the user
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    
    # Always redirect to login page
    return redirect('login')

@login_required
def dashboard(request):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    # Get user's medicines
    medicines = Medicine.objects.filter(user=request.user)
    
    # Calculate statistics
    total_medicines = medicines.count()
    expired_medicines = medicines.filter(expiry_date__lt=timezone.now().date()).count()
    expiring_soon = medicines.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date()
    ).count()
    low_stock = medicines.filter(quantity__lte=F('low_stock_threshold')).count()
    
    # Get recent medicines
    recent_medicines = medicines[:5]
    
    # Get alerts
    expired_list = medicines.filter(expiry_date__lt=timezone.now().date())[:5]
    expiring_soon_list = medicines.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date()
    )[:5]
    low_stock_list = medicines.filter(quantity__lte=F('low_stock_threshold'))[:5]
    
    context = {
        'total_medicines': total_medicines,
        'expired_medicines': expired_medicines,
        'expiring_soon': expiring_soon,
        'low_stock': low_stock,
        'recent_medicines': recent_medicines,
        'expired_list': expired_list,
        'expiring_soon_list': expiring_soon_list,
        'low_stock_list': low_stock_list,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def medicine_list(request):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    medicines = Medicine.objects.filter(user=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(batch_number__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )
    
    # Filter functionality
    filter_type = request.GET.get('filter', '')
    if filter_type == 'expired':
        medicines = medicines.filter(expiry_date__lt=timezone.now().date())
    elif filter_type == 'expiring_soon':
        medicines.filter(
            expiry_date__lte=timezone.now().date() + timedelta(days=30),
            expiry_date__gt=timezone.now().date()
        )
    elif filter_type == 'low_stock':
        medicines = medicines.filter(quantity__lte=F('low_stock_threshold'))
    
    context = {
        'medicines': medicines,
        'search_query': search_query,
        'filter_type': filter_type,
    }
    return render(request, 'inventory/medicine_list.html', context)

@login_required
def add_medicine(request):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            medicine.save()
            messages.success(request, f'Medicine "{medicine.name}" added successfully!')
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'inventory/medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
def edit_medicine(request, pk):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medicine "{medicine.name}" updated successfully!')
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'inventory/medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

@login_required
def delete_medicine(request, pk):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, f'Medicine "{medicine.name}" deleted successfully!')
        return redirect('medicine_list')
    return render(request, 'inventory/medicine_confirm_delete.html', {'medicine': medicine})

@login_required
def alerts(request):
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    medicines = Medicine.objects.filter(user=request.user)
    
    expired_medicines = medicines.filter(expiry_date__lt=timezone.now().date())
    expiring_soon_medicines = medicines.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date()
    )
    low_stock_medicines = medicines.filter(quantity__lte=F('low_stock_threshold'))
    
    context = {
        'expired_medicines': expired_medicines,
        'expiring_soon_medicines': expiring_soon_medicines,
        'low_stock_medicines': low_stock_medicines,
    }
    return render(request, 'inventory/alerts.html', context)

@login_required
def reports(request):
    """Reports page with download options"""
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    # Get summary statistics
    report_generator = MedicineReportGenerator(request.user)
    summary = report_generator.get_inventory_summary()
    
    context = {
        'summary': summary,
    }
    return render(request, 'inventory/reports.html', context)

@login_required
def download_report(request, report_type, format_type):
    """Download report in specified format"""
    # Check if user's email is verified
    profile = get_or_create_user_profile(request.user)
    if not profile.email_verified:
        messages.warning(request, 'Please verify your email address to access all features.')
        return redirect('resend_verification')
    
    # Validate report type
    valid_report_types = ['all', 'expired', 'expiring_soon', 'low_stock', 'active']
    if report_type not in valid_report_types:
        messages.error(request, 'Invalid report type.')
        return redirect('reports')
    
    # Validate format type
    valid_formats = ['pdf', 'excel']
    if format_type not in valid_formats:
        messages.error(request, 'Invalid format type.')
        return redirect('reports')
    
    # Generate report
    report_generator = MedicineReportGenerator(request.user)
    
    try:
        if format_type == 'excel':
            return report_generator.generate_excel_report(report_type)
        elif format_type == 'pdf':
            return report_generator.generate_pdf_report(report_type)
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('reports')
