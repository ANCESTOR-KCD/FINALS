from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


SESSION_CHOICES = [
    ('2022/2023', '2022/2023'),
    ('2021/2022', '2021/2022'),
    ('2020/2021', '2020/2021'),
    ('2019/2020', '2019/2020'),
    ('2018/2019', '2018/2019'),
]


ENGINEERING_COURSES = [
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
    # Add more courses as needed
]


class UserManager(BaseUserManager):
    def create_user(self, matric_number, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            matric_number=matric_number,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            matric_number='1234',  # Default matriculation number for admins
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    matric_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



courses = [
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
    # Add more courses as needed
]
class Session(models.Model):
    name = models.CharField(max_length=9, unique=True)  # Max length is 9 to handle 'YYYY/YYYY'

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles' , null=True, blank=True)  # Allow multiple profiles per user
    current_year_of_study = models.IntegerField(default=1, null=True, blank=True)  # Default to 1st year, can be null
    school_fees_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    dept_fees_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    faculty_fees_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    matriculation_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True, default='2022-01-01')
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    state_of_origin = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    lga = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.matric_number}'s profile"



#course registration

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_title = models.CharField(max_length=100)
    credit_load = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"


class CourseRegistration(models.Model):
    session = models.CharField(max_length=20)
    reference_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=20)
    current_year_of_study = models.IntegerField()
    gender = models.CharField(max_length=10)
    courses = models.ManyToManyField(Course)
    total_credit_load = models.IntegerField(default=0)

    def __str__(self):
        return f"Course Registration for {self.name} ({self.reg_number}) - {self.session}"

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ConfirmFees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_fees_receipt = models.ImageField(upload_to='receipts/')
    dept_fees_receipt = models.ImageField(upload_to='receipts/')
    faculty_fees_receipt = models.ImageField(upload_to='receipts/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fee confirmation for {self.user.username} on {self.created_at}"
    
    
    