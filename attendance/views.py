from django.shortcuts import render
from attendance.serializers import OverallAttendanceSerializer,AttendanceRecordSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section


# Create your views here.

class OverallAttendanceView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = OverallStudentAttendance.objects.all()
    serializer_class = OverallAttendanceSerializer

class AttendanceRecordView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer