from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teacher.serializers import OverallAttendanceSerializer,AttendanceRecordSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
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
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication])
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
        data = request.data
        courseObject = Course.objects.get(course_id=data["course"])
        students = data["students"]

        for student in students:
            studentObject = Student.objects.get(usn=student["studentUsn"])
            AttendanceRecord.objects.create(is_present= student['is_present'], course=courseObject, student=studentObject)
            overallAttendanceObject, _ = OverallStudentAttendance.objects.get_or_create(student=studentObject, course=courseObject, defaults={"total_classes":0, "total_present":0})
            overallAttendanceObject.total_classes+=1
            if student["is_present"]:
                overallAttendanceObject.total_present+=1
            overallAttendanceObject.save()

        return Response("Successful")
    except Exception as ex:
        return Response(ex)

