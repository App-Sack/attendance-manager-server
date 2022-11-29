"""
URL mappings for the attendance API.
"""
from django.urls import include, path
from rest_framework import routers

from attendance import views

router = routers.DefaultRouter()
router.register(r'overallAttendance', views.OverallAttendanceView)
router.register(r'attendanceRecord',views.AttendanceRecordView)


urlpatterns = [
    path('', include(router.urls)),
    path('add-bulk-attendance', views.add_bulk_attendance)
]