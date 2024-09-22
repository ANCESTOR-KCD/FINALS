from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, CourseRegistration, ConfirmFees, Course


# Define the choices for school years
SCHOOL_YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
    ('5', '5th Year'),
]

# Define the choices for sessions
SESSION_CHOICES = [
    ('2022/2023', '2022/2023'),
    ('2021/2022', '2021/2022'),
    ('2020/2021', '2020/2021'),
    ('2019/2020', '2019/2020'),
]



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, CourseRegistration, ConfirmFees

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Enter your email'
        })
    )
    matric_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Matriculation Number'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ('matric_number', 'email', 'password1', 'password2')

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'current_year_of_study', 'gender', 'school_fees_receipt', 'dept_fees_receipt', 'faculty_fees_receipt', 
            'full_name', 'matriculation_number', 'email', 'phone_number', 'birth_date', 'address', 
            'nationality', 'state_of_origin', 'town', 'lga', 'picture'
        ]
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Prefer not to say')]),
            'picture': forms.ClearableFileInput(attrs={'onchange': 'previewImage(event)', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'matriculation_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'state_of_origin': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),
            'lga': forms.TextInput(attrs={'class': 'form-control'}),
        }






from django import forms
from .models import CourseRegistration

class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = ['session', 'reference_number', 'name', 'reg_number', 'current_year_of_study', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removed the reference to self.fields['courses']
    
    # Removed the clean_courses method, as courses are handled in the view

    # Removed the save logic for courses, since they are being handled in the view



        

class ConfirmFeesForm(forms.ModelForm):
    class Meta:
        model = ConfirmFees
        fields = ['school_fees_receipt', 'dept_fees_receipt', 'faculty_fees_receipt']
