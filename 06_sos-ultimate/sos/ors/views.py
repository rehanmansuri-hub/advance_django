from django.http import HttpResponse
from django.shortcuts import render, redirect
from .ctl.registration_ctl import RegistrationCtl
from .ctl.login_ctl import LoginCtl
from .ctl.welcome_ctl import WelcomeCtl
from .ctl.user_ctl import UserCtl
from .ctl.user_list_ctl import UserListCtl
from .ctl.role_ctl import RoleCtl
from .ctl.role_list_ctl import RoleListCtl
from .ctl.college_ctl import CollegeCtl
from .ctl.college_list_ctl import CollegeListCtl
from .ctl.student_ctl import StudentCtl
from .ctl.student_list_ctl import StudentListCtl
from .ctl.course_ctl import CourseCtl
from .ctl.course_list_ctl import CourseListCtl
from .ctl.faculty_ctl import FacultyCtl
from .ctl.faculty_list_ctl import FacultyListCtl
from .ctl.subject_ctl import SubjectCtl
from .ctl.marksheet_list_ctl import MarksheetListCtl
from .ctl.marksheet_ctl import MarksheetCtl
from .ctl.subject_list_ctl import SubjectListCtl
from .ctl.timetable_ctl import TimeTableCtl
from .ctl.timetable_list_ctl import TimeTableListCtl
from .utility.html_utility import HtmlUtility


def welcome(request):
    return render(request, 'welcome.html')


def user_logout(request):
    request.session.flush()
    return redirect('/ors/Login/')


def action(request, page):
    if 'favicon.ico' in request.path:
        return HttpResponse(status=204)
    ctl_name = page + "Ctl()"
    ctl_obj = eval(ctl_name)
    return ctl_obj.execute(request, params={'operation': '', 'id': 0})


def action_operation_id(request, page, operation='', id=0):
    if 'favicon.ico' in request.path:
        return HttpResponse(status=204)
    ctl_name = page + "Ctl()"
    ctl_obj = eval(ctl_name)
    return ctl_obj.execute(request, params={'operation': operation, 'id': id})


def test_html_utility(request):
    gender_list = ["Male", "Female"]
    html = HtmlUtility.get_list_from_list("gender", "Male", gender_list)
    print(html)
    return HttpResponse(html)