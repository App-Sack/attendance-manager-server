"""
URL mappings for the attendance API.
"""
from django.urls import include, path
from rest_framework import routers

from teacher import views

# router = routers.DefaultRouter()
# router.register(r'overallAttendance', views.OverallAttendanceView)
# router.register(r'me',views.TeacherView)


urlpatterns = [
    # path('', include(router.urls)),
    path('add-bulk-attendance', views.add_bulk_attendance),
    path('reset-attendance-on-date', views.reset_attendance_on_date),
    path('get-teacher-details/<str:teacherEmail>/', views.get_teacher_details),
    path("get-students-in-section/<str:section>/<str:courseId>/", views.get_students_in_section),
]