from rest_framework import serializers
from core.models import User, Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section



class OverallAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = OverallStudentAttendance
        fields = "__all__"
        
class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializer for Attendance Record Object"""

    class Meta:
        model=AttendanceRecord
        fields="__all__"