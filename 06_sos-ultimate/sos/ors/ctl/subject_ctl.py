from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.models import Subject
from ors.service.subject_service import SubjectService
from ors.utility.data_validator import DataValidator

from ..service.course_service import CourseService
from ..utility.html_utility import HtmlUtility


class SubjectCtl(BaseCtl):

    def preload(self, request):
        course_list = CourseService().search({})

        preload_data = {}

        preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId",
            int(self.form.get("course_id") or 0),
            course_list
        )
        return preload_data

    def request_to_form(self, request):
        self.form['id'] = int(request.POST.get('id') or 0)
        self.form['name'] = request.POST.get('name', '').strip()
        self.form['description'] = request.POST.get('description', '').strip()
        self.form["course_id"] = request.POST.get("course_id", 0)


    def form_to_model(self, obj):
        obj.id = self.form['id']
        obj.name = self.form['name']
        obj.description = self.form['description']

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form["course_id"] = int(obj.course_id) if obj.course_id else 0


    def input_validation(self, request):
        input_error = self.form.get('input_error')
        input_error['error'] = False

        if DataValidator.is_null(self.form.get('name')):
            input_error['name'] = 'Name is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('description')):
            input_error['description'] = 'Description is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get("course_id")) or self.form.get("course_id") == "0":
            input_error["course_id"] = "Course can not be null"
            input_error['error'] = True

        return input_error['error']

    def display(self, request, params={}):
        return render(
            request,
            self.get_template(),
            {
                'form': self.form,
                'preload_data': self.preload(request)
            }
        )

    def submit(self, request, params={}):
        try:
            subject = self.form_to_model(Subject())
            self.get_service().save(subject)

            self.model_to_form(subject)

            if self.form['id'] > 0:
                self.form['message'] = "Subject Updated Successfully...!!!"
            else:
                self.form['message'] = "Subject Added Successfully...!!!"

            self.form['error'] = False

        except Exception as e:
            self.form['message'] = str(e)
            self.form['error'] = True

        return render(
            request,
            self.get_template(),
            {
                'form': self.form,
                'preload_data': self.preload(request)
            }
        )

    def get_service(self):
        return SubjectService()

    def get_template(self):
        return "subject.html"