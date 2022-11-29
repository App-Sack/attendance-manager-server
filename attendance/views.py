from django.shortcuts import render
from attendance.serializers import OverallAttendanceSerializer,AttendanceRecordSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


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

@api_view(["POST"])
def add_bulk_attendance(request):
    """Data should come in this format:"""
    """ { "course":"20cs110", "students" : [
            {
                "is_present" : true,
                "studentUsn" : "01jst20cs036"
            },
            {
                "is_present" : false,
                "studentUsn" : "01jst20cs036"
            }
    ] } """
    try:
        data = json.loads(request.body)
        course = Course.objects.get(course_id=data["course"])
        students = data["students"]
        for student in students:
            studentObject = Student.objects.get(usn=student["studentUsn"])
            AttendanceRecord.objects.create(is_present= student['is_present'], course=course, student=studentObject)
        return Response("Successful")
    except Exception as ex:
        return Response(ex)

