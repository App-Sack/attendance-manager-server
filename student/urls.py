from django.urls import include, path
from rest_framework import routers

from student import views

router = routers.DefaultRouter()
router.register(r'',views.StudentView)

urlpatterns = [
    path('',include(router.urls)),
]
