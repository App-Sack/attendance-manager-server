from rest_framework import serializers
from core.models import User, Student, Course, Semester, AttendanceRecord, OverallStudentAttendance, Section

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for the Student object."""

    class Meta:
        model=Student
        fields="__all__"
