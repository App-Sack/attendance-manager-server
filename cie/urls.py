from django.urls import include, path
from rest_framework import routers

from cie import views


urlpatterns = [
    path("get-students-in-section-cie/<str:section>/<str:courseId>/", views.get_students_in_section_cie),
    path("get-students-all-courses-cie/<str:usn>/", views.get_student_all_courses_cie),
    path("update-student-cie/", views.update_student_cie),
]
