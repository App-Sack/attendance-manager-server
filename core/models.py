from django.db import models

# Create your models here.
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

class Semester(models.Model):
    sem = models.CharField(max_length=5,choices=SEMESTER_CHOICES, unique=True, primary_key=True)

    def __str__(self):
        return self.sem


class Section(models.Model):
    section = models.CharField(max_length=5)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.section


class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=25, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course)
    #sections = models.ManyToManyField(Section)

    def __str__(self):
        return self.name


class Student(models.Model):
    usn = models.CharField(max_length = 15, unique=True, primary_key=True)
    sr_no = models.CharField(max_length = 15, unique=True)
    name = models.CharField(max_length=255)
    sem = models.OneToOneField(Semester, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name  + ' '   + self.course.name


class OverallStudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_classes = models.IntegerField()
    total_present = models.IntegerField()

    # def __str__(self):
    #     return self.student.name + " - " + self.course.name + " - " + str(self.total_classes)