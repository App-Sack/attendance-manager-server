from django.urls import include, path
from rest_framework import routers

from student import views

router = routers.DefaultRouter()
router.register(r'',views.StudentView)

urlpatterns = [
    path('',include(router.urls)),
    path('get-student-attendance-cie/<str:studentUsn>/', views.get_student_attendance_cie),
    path("get-calendar-attendance/<str:studentUsn>/<str:courseId>/", views.get_calendar_attendance)
]
