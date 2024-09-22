from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm, CourseRegistrationForm, ConfirmFeesForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import ConfirmFees, Course, CourseRegistration, Profile

@login_required
def home(request):
    return render(request, 'students/home.html')

from django.contrib.auth import login
from django.contrib.auth import get_backends

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Get the first available authentication backend and use it for login
            backend = get_backends()[1]
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(request, user, backend=user.backend)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'students/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'students/login.html')

@login_required
def profile(request):
    try:
        profile = request.user.profiles
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'students/profile.html', {'form': form, 'profile': profile})

@login_required
def course_registration(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            # Redirect to the preview page without a pk
            request.session['selected_courses'] = valid_courses
            request.session['total_credit_load'] = total_credit_load
            return redirect('course_registration_preview')

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseRegistrationForm()
    return render(request, 'students/course_registration.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConfirmFeesForm
from .models import ConfirmFees

@login_required
def confirm_fees(request):
    # Get all ConfirmFees objects for the user, ordered by creation date
    confirm_fees_objects = ConfirmFees.objects.filter(user=request.user).order_by('-created_at')
    
    # Use the most recent one if it exists, otherwise None
    instance = confirm_fees_objects.first()

    if request.method == 'POST':
        form = ConfirmFeesForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            confirm_fees_instance = form.save(commit=False)
            confirm_fees_instance.user = request.user
            confirm_fees_instance.save()
            messages.success(request, 'Fees confirmed successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConfirmFeesForm(instance=instance)

    context = {
        'form': form,
        'confirm_fees_objects': confirm_fees_objects,
    }
    return render(request, 'students/confirm_fees.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'students/change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def course_registration_preview(request):
    selected_courses = request.session.get('selected_courses', [])
    total_credit_load = request.session.get('total_credit_load', 0)

    return render(request, 'students/course_registration_preview.html', {
        'selected_courses': selected_courses,
        'total_credit_load': total_credit_load
    })

@login_required
def list_profiles(request):
    user_profiles = Profile.objects.filter(user=request.user).order_by('-session')
    return render(request, 'students/list_profiles.html', {'profiles': user_profiles})



@login_required
def course_registration(request):
    course_data = [
    {"course_code": "ENG101", "course_title": "Introduction to Engineering", "credit_load": 3},
    {"course_code": "ENG102", "course_title": "Engineering Mathematics I", "credit_load": 3},
    {"course_code": "ENG103", "course_title": "Physics for Engineers", "credit_load": 4},
    {"course_code": "ENG104", "course_title": "Engineering Drawing", "credit_load": 2},
    {"course_code": "ENG201", "course_title": "Engineering Mathematics II", "credit_load": 3},
    {"course_code": "ENG202", "course_title": "Thermodynamics", "credit_load": 3},
    {"course_code": "ENG203", "course_title": "Mechanics of Materials", "credit_load": 3},
    {"course_code": "ENG204", "course_title": "Fluid Mechanics", "credit_load": 3},
    {"course_code": "ENG301", "course_title": "Electrical Engineering", "credit_load": 3},
    {"course_code": "ENG302", "course_title": "Control Systems", "credit_load": 3},
    {"course_code": "ENG303", "course_title": "Heat Transfer", "credit_load": 3},
    {"course_code": "ENG304", "course_title": "Engineering Design", "credit_load": 3},
    {"course_code": "ENG401", "course_title": "Engineering Project", "credit_load": 6},
    {"course_code": "ENG402", "course_title": "Environmental Engineering", "credit_load": 3},
    {"course_code": "ENG403", "course_title": "Manufacturing Processes", "credit_load": 3},
    {"course_code": "ENG404", "course_title": "Engineering Management", "credit_load": 3},
    {"course_code": "ENG405", "course_title": "Capstone Design Project", "credit_load": 6},
    {"course_code": "ENG406", "course_title": "Finite Element Analysis", "credit_load": 3},
    {"course_code": "ENG407", "course_title": "Structural Analysis", "credit_load": 3},
    {"course_code": "ENG408", "course_title": "Advanced Control Systems", "credit_load": 4},
    {"course_code": "ENG409", "course_title": "Engineering Ethics", "credit_load": 2},
    {"course_code": "ENG410", "course_title": "Hydraulic Engineering", "credit_load": 3},
    {"course_code": "ENG411", "course_title": "Geotechnical Engineering", "credit_load": 3},
    {"course_code": "ENG412", "course_title": "Machine Design", "credit_load": 3},
    {"course_code": "ENG413", "course_title": "Advanced Thermodynamics", "credit_load": 3},
    {"course_code": "ENG414", "course_title": "Computational Fluid Dynamics", "credit_load": 4},
    {"course_code": "ENG415", "course_title": "Power Systems Engineering", "credit_load": 3},
    {"course_code": "ENG416", "course_title": "Renewable Energy Systems", "credit_load": 3},
    {"course_code": "ENG417", "course_title": "Robotics Engineering", "credit_load": 4},
    {"course_code": "ENG418", "course_title": "Mechatronics", "credit_load": 3},
    {"course_code": "ENG419", "course_title": "Advanced Manufacturing", "credit_load": 3},
    {"course_code": "ENG420", "course_title": "Nanotechnology", "credit_load": 3},
    {"course_code": "ENG421", "course_title": "Biomedical Engineering", "credit_load": 3}
]
    
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        
        selected_courses = request.POST.getlist('courses')  # Get selected course codes
        
        valid_courses = []
        total_credit_load = 0
        for course_code in selected_courses:
            course = next((course for course in course_data if course['course_code'] == course_code), None)
            if course:
                valid_courses.append(course)
                total_credit_load += course['credit_load']

        if not valid_courses:
            messages.error(request, 'You must select at least one valid course.')
        elif total_credit_load > 24:
            messages.error(request, 'Total credit load cannot exceed 24 credits.')
        else:
            # If valid, redirect to preview page with selected courses in session
            request.session['selected_courses'] = valid_courses
            request.session['total_credit_load'] = total_credit_load
            return redirect('course_registration_preview')

    else:
        form = CourseRegistrationForm()

    context = {
        'form': form,
        'course_data': course_data,
    }
    return render(request, 'students/course_registration.html', context)
