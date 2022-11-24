from django.contrib import admin

# Register your models here.
from .models import Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section

class StudentAdmin(admin.ModelAdmin):
    list_display = ['usn', 'sr_no', 'name', 'sem', 'section']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'name']

class OverallStudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'total_classes', 'total_present']

class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'is_present']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'name', 'sem']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['section', 'sem']

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester)
admin.site.register(Section, SectionAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(OverallStudentAttendance, OverallStudentAttendanceAdmin)
