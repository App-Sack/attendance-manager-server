from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teacher.serializers import OverallAttendanceSerializer,TeacherSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Cie, Semester, AttendanceRecord, OverallStudentAttendance, Section, AssignedClasses
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.


@api_view(["GET"])
def get_students_in_section_cie(request, section, courseId):
    try:
        sectionObj = Section.objects.get(section=section)
        courseObj = Course.objects.get(course_id=courseId)
        students = Student.objects.filter(section=sectionObj).order_by('usn')

        studentsData = []

        for student in students:
            cie, created = Cie.objects.get_or_create(student=student, course=courseObj, section=sectionObj )
            studentsData.append({"usn":student.usn,"name":student.name,"e1":cie.e1,"e2":cie.e2,"e3":cie.e3,"e4":cie.e4,"e5":cie.e5})

        responseData = {"course_id":courseId, "students_data":studentsData}
        return Response(responseData)
    except Exception as ex:
        return Response(str(ex))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication])
def update_student_cie(request):
    """Data should come in this format:
    {
        "usn":"01jst20cs036",
        "course_id":"20cs552",
        "e1":23,
        "e2":23,
        "e3":23,
        "e4":23,
        "e5":23
    } """
    try:
        data = request.data
        student = Student.objects.get(usn=data["usn"])
        course = Course.objects.get(course_id=data["course_id"])

        cieRecord, created = Cie.objects.get_or_create(student=student,course=course,section=student.section)
        cieRecord.e1 = data["e1"]
        cieRecord.e2 = data["e2"]
        cieRecord.e3 = data["e3"]
        cieRecord.e4 = data["e4"]
        cieRecord.e5 = data["e5"]

        cieRecord.save()

        return Response("Successful")
    except Exception as ex:
        return Response(str(ex))
