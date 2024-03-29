"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student, Department, Course, Semester, AttendanceRecord, OverallStudentAttendance, Section, AssignedClasses, Cie

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'dept', 'is_staff', 'is_hod']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name','dept')}),
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
                'dept',
                'is_active',
                'is_staff',
                'is_hod',
                'is_superuser',
            ),
        }),
    )




class StudentAdmin(admin.ModelAdmin):
    list_display = ['usn', 'sr_no', 'name','section', 'parent_phone_number']
    search_fields = ['usn', 'sr_no', 'name']
    list_filter = (
        ('section', admin.RelatedOnlyFieldListFilter),
        ('section__dept', admin.RelatedOnlyFieldListFilter),
    )

class OverallStudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'total_classes', 'total_present', 'attendance_percentage']
    list_filter = (
        ('course', admin.RelatedOnlyFieldListFilter),
        ('student__section', admin.RelatedOnlyFieldListFilter),
    )

    def attendance_percentage(self, obj):
        return round((obj.total_present/obj.total_classes)*100,2) if obj.total_classes!=0 else None

class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'is_present']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'name', 'sem']
    list_filter = (
        ('course_dept', admin.RelatedOnlyFieldListFilter),
        ('sem', admin.RelatedOnlyFieldListFilter),
    )

class SectionAdmin(admin.ModelAdmin):
    list_display = ['section', 'sem', 'dept']

class AssignedClassesAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'course', 'section']

class CieAdmin(admin.ModelAdmin):
    list_display = ['student', 'section', 'course', 'e1', 'e2', 'e3',]
    list_filter = (
        ('course', admin.RelatedOnlyFieldListFilter),
        ('section', admin.RelatedOnlyFieldListFilter),
    )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_short_name', 'dept_full_name', 'hod']


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Semester)
admin.site.register(AssignedClasses, AssignedClassesAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(OverallStudentAttendance, OverallStudentAttendanceAdmin)
admin.site.register(Cie, CieAdmin)
admin.site.register(Department, DepartmentAdmin)


# Customizing Django Admin Site
admin.site.site_header = "SJCE Attendance Admin Panel"
admin.site.site_title = "SJCE Attendance Portal"
admin.site.index_title = "Welcome to SJCE Attendance Portal"
