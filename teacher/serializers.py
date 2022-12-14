from rest_framework import serializers
from core.models import User, Student, Course, Semester, AttendanceRecord, OverallStudentAttendance, Section



class OverallAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = OverallStudentAttendance
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher Object"""

    class Meta:
        model=User
        fields="__all__"