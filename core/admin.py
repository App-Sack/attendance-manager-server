"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student, Course, Semester, AttendanceRecord, OverallStudentAttendance, Section, AssignedClasses, Cie

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'is_staff', 'is_hod']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_hod',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_hod',
                'is_superuser',
            ),
        }),
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ['usn', 'sr_no', 'name','section']

class OverallStudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'total_classes', 'total_present']

class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'is_present']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'name', 'sem']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['section', 'sem']

class AssignedClassesAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'course', 'section']

class CieAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'e1', 'e2', 'e3', 'e4', 'e5']


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester)
admin.site.register(AssignedClasses, AssignedClassesAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(OverallStudentAttendance, OverallStudentAttendanceAdmin)
admin.site.register(Cie, CieAdmin)


# Customizing Django Admin Site
admin.site.site_header = "SJCE Attendance Admin Panel"
admin.site.site_title = "SJCE Attendance Portal"
admin.site.index_title = "Welcome to SJCE Attendance Portal"
