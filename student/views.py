from student.serializers import StudentSerializer
from rest_framework import viewsets, authentication, permissions
from core.models import User, Student, Course, Teacher, Semester, AttendanceRecord, OverallStudentAttendance, Section
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class StudentView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@api_view(["GET"])
def get_student_attendance(request, studentUsn):
    try:
        attendance_list = []
        student = Student.objects.get(usn=studentUsn)
        coursesStudentHasEnrolled = student.courses.all()
        for courseObj in coursesStudentHasEnrolled:
            attendance, created = OverallStudentAttendance.objects.get_or_create(student=student, course=courseObj, defaults={"total_classes":0, "total_present":0})
            if attendance is None:
                continue
            attendance_list.append({"courseName":courseObj.name, "courseCode":courseObj.course_id, "totalClasses": attendance.total_classes, "totalPresent":attendance.total_present})
        return Response(attendance_list)
    except Exception as ex:
        return Response(str(ex))


@api_view(["GET"])
def get_calendar_attendance(request, studentUsn, courseId):
    try:
        studentObj = Student.objects.get(usn=studentUsn)
        courseObj = Course.objects.get(course_id=courseId)
        print(1)
        records = AttendanceRecord.objects.filter(student=studentObj,course=courseObj)
        print(2)
        print(records)
        responseData = []
        for record in records:
            responseData.append({"date":record.date, "isPresent":record.is_present})
        return Response(responseData)
    except Exception as ex:
        return Response(str(ex))