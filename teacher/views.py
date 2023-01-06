from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from teacher.serializers import OverallAttendanceSerializer,TeacherSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Semester, AttendanceRecord, OverallStudentAttendance, Section, AssignedClasses
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.

class OverallAttendanceView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = OverallStudentAttendance.objects.all()
    serializer_class = OverallAttendanceSerializer

class TeacherView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = TeacherSerializer



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication])
def add_bulk_attendance(request):
    """Data should come in this format:
    { "course":"20cs110", "no_of_classes":2, "students" : [
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
        no_of_classes = data["no_of_classes"]

        for i in range(no_of_classes):
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
        return Response(str(ex))


@api_view(["GET"])
def get_teacher_details(request, teacherEmail):
    teacherObj = User.objects.get(email=teacherEmail)
    responseData = {}
    responseData["email"]=teacherObj.email
    responseData["name"]=teacherObj.name
    responseData["assignedClasses"]=[]
    assignedClassObjs = AssignedClasses.objects.filter(teacher=teacherObj)

    for assignedClassObj in assignedClassObjs:
        responseData["assignedClasses"].append({"section":assignedClassObj.section.section, "courseName":assignedClassObj.course.name, "courseId":assignedClassObj.course.course_id})

    return Response(responseData)


@api_view(["GET"])
def get_students_in_section(request, section, courseId):
    try:
        sectionObj = Section.objects.get(section=section)
        courseObj = Course.objects.get(course_id=courseId)
        students = Student.objects.filter(section=sectionObj).order_by('usn')
        studentsData = []
        for student in students:
            attendance, created = OverallStudentAttendance.objects.get_or_create(student=student, course=courseObj, defaults={"total_classes":0, "total_present":0})
            studentAttendancePercentage = 0
            if attendance.total_classes>0:
                studentAttendancePercentage = round((attendance.total_present/attendance.total_classes)*100,2)
            studentsData.append({"usn":student.usn,"name":student.name,"total_classes":attendance.total_classes,"total_present":attendance.total_present,"attendance_percentage":studentAttendancePercentage})
        responseData = {"course_id":courseId, "students_data":studentsData}
        return Response(responseData)
    except Exception as ex:
        return Response(str(ex))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication])
def reset_attendance_on_date(request):
    """Data should come in this format:
    {
        "course_id":"20cs510",
        "usn":"01jst20cs036",
        "date": "2023-01-06"
    } """
    try:
        data = request.data
        courseObj = Course.objects.get(course_id=data["course_id"])
        studentObj = Student.objects.get(usn=data["usn"])
        date = data["date"]

        overallAttendance = OverallStudentAttendance.objects.get(student=studentObj, course=courseObj)
        attendanceRecords = AttendanceRecord.objects.filter(student=studentObj, course=courseObj, date__icontains=date).all()

        for record in attendanceRecords:
            overallAttendance.total_classes-=1
            if record.is_present==True:
                overallAttendance.total_present-=1

        overallAttendance.save()
        attendanceRecords.delete()

        return Response("Successful")
    except Exception as ex:
        return Response(str(ex))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication, authentication.SessionAuthentication, authentication.BasicAuthentication])
def add_single_attendance_on_date(request):
    """
    Sample post data
    Send date in this format - (YYYY-MM-DD)
    {
        "usn":"01jst20cs036",
        "course_id":"20cs510",
        "date":"2023-01-06",
        "is_present":true
    }
    """
    try:
        data = request.data
        studentObj = Student.objects.get(usn=data["usn"])
        courseObj = Course.objects.get(course_id=data["course_id"])
        date = data["date"]
        is_present = data["is_present"]

        AttendanceRecord(student=studentObj,course=courseObj, date=date, is_present=is_present).save()

        overallAttendance = OverallStudentAttendance.objects.get(student=studentObj, course=courseObj)
        overallAttendance.total_classes+=1

        if is_present==True:
            overallAttendance.total_present+=1

        overallAttendance.save()

        return Response("Successful")
    except Exception as ex:
        return Response(str(ex))