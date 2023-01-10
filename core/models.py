"""
DB Models
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)

class UserManager(BaseUserManager):
    """Manager for Users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User Must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the System"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_hod = models.BooleanField(default=False)
    dept = models.ForeignKey("Department",on_delete=models.SET_NULL,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Staff'

class Department(models.Model):
    dept_short_name = models.CharField(max_length=50,primary_key=True)
    dept_full_name = models.CharField(max_length=255)
    hod = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.dept_short_name

class Semester(models.Model):
    sem = models.CharField(max_length=5,choices=SEMESTER_CHOICES, unique=True, primary_key=True)

    def __str__(self):
        return self.sem


class Section(models.Model):
    section = models.CharField(max_length=5, primary_key= True)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course')
    dept = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.section} - {self.dept}"


class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)
    course_dept = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.course_id


class AssignedClasses(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

class Student(models.Model):
    usn = models.CharField(max_length = 15, unique=True, primary_key=True)
    sr_no = models.CharField(max_length = 15, unique=True)
    name = models.CharField(max_length=255)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    dob = models.CharField(max_length=50)
    parent_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student.name  + ' '   + self.course.name


class OverallStudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_classes = models.IntegerField()
    total_present = models.IntegerField()

    # def __str__(self):
    #     return self.student.name + " - " + self.course.name + " - " + str(self.total_classes)

class Cie(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    e1 = models.SmallIntegerField(null=True, blank=True)
    e2 = models.SmallIntegerField(null=True, blank=True)
    e3 = models.SmallIntegerField(null=True, blank=True)
    e4 = models.SmallIntegerField(null=True, blank=True)
    e5 = models.SmallIntegerField(null=True, blank=True)

