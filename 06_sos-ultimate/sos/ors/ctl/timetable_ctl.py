from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.models import TimeTable
from ors.service.timetable_service import TimeTableService
from ors.utility.data_validator import DataValidator

from ..service.course_service import CourseService
from ..service.subject_service import SubjectService
from ..utility.html_utility import HtmlUtility


class TimeTableCtl(BaseCtl):

    def preload(self, request):

        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

        preload_data = {}

        preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_id",
            int(self.form.get("course_id") or 0),
            course_list
        )

        preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subject_id",
            int(self.form.get("subject_id") or 0),
            subject_list
        )

        return preload_data

    def request_to_form(self, request):

        self.form["id"] = int(request.POST.get("id") or 0)
        self.form["exam_date"] = request.POST.get("exam_date", "")
        self.form["exam_time"] = request.POST.get("exam_time", "")
        self.form["semester"] = request.POST.get("semester", "")
        self.form["course_id"] = request.POST.get("course_id", 0)
        self.form["subject_id"] = request.POST.get("subject_id", 0)

    def form_to_model(self, obj):

        obj.id = self.form["id"]
        obj.exam_date = self.form["exam_date"]
        obj.exam_time = self.form["exam_time"]
        obj.semester = self.form["semester"]

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id)
        obj.course_name = course.name if course else ""

        subject_id = int(self.form.get("subject_id") or 0)
        obj.subject_id = subject_id

        subject = SubjectService().get(subject_id)
        obj.subject_name = subject.name if subject else ""

        return obj

    def model_to_form(self, obj):

        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["exam_date"] = obj.exam_date
        self.form["exam_time"] = obj.exam_time
        self.form["semester"] = obj.semester
        self.form["course_id"] = obj.course_id
        self.form["subject_id"] = obj.subject_id

    def input_validation(self, request):

        input_error = self.form.get("input_error")
        input_error["error"] = False

        if DataValidator.is_null(self.form.get("exam_date")):
            input_error["exam_date"] = "Exam Date is required"
            input_error["error"] = True

        if DataValidator.is_null(self.form.get("exam_time")):
            input_error["exam_time"] = "Exam Time is required"
            input_error["error"] = True

        if DataValidator.is_null(self.form.get("semester")):
            input_error["semester"] = "Semester is required"
            input_error["error"] = True

        if self.form.get("course_id") == "0":
            input_error["course_id"] = "Course is required"
            input_error["error"] = True

        if self.form.get("subject_id") == "0":
            input_error["subject_id"] = "Subject is required"
            input_error["error"] = True

        return input_error["error"]

    def display(self, request, params={}):
        return render(
            request,
            self.get_template(),
            {
                "form": self.form,
                "preload_data": self.preload(request)
            }
        )

    def submit(self, request, params={}):

        try:
            timetable = self.form_to_model(TimeTable())
            self.get_service().save(timetable)

            self.model_to_form(timetable)

            self.form["message"] = "TimeTable Saved Successfully"
            self.form["error"] = False

        except Exception as e:
            self.form["message"] = str(e)
            self.form["error"] = True

        return render(
            request,
            self.get_template(),
            {
                "form": self.form,
                "preload_data": self.preload(request)
            }
        )

    def get_service(self):
        return TimeTableService()

    def get_template(self):
        return "timetable.html"