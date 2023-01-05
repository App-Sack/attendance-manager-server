from django.urls import include, path
from rest_framework import routers

from cie import views


urlpatterns = [
    path("get-students-in-section-cie/<str:section>/<str:courseId>/", views.get_students_in_section),
]
    