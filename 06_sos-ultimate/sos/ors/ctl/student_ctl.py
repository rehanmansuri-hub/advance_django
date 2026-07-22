from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.models import Student
from ors.service.college_service import CollegeService
from ors.service.student_service import StudentService
from ors.utility.data_validator import DataValidator
from ors.utility.html_utility import HtmlUtility


class StudentCtl(BaseCtl):

    def preload(self, request):
        gender_list = ['Male', 'Female']
        college_list = CollegeService().search({'page_size': 0})

        self.form['preload_data']['gender_select'] = HtmlUtility.get_list_from_list(
            'gender',
            self.form.get('gender'),
            gender_list
        )

        self.form['preload_data']['college_select'] = HtmlUtility.get_list_from_beans(
            'collegeId',
            int(self.form.get('college_id') or 0),
            college_list
        )

    def request_to_form(self, request):
        self.form['id'] = int(request.POST.get('id') or 0)
        self.form['first_name'] = request.POST.get('firstName', '').strip()
        self.form['last_name'] = request.POST.get('lastName', '').strip()
        self.form['email'] = request.POST.get('email', '').strip()
        self.form['mobile_no'] = request.POST.get('mobileNo', '').strip()
        self.form['dob'] = request.POST.get('dob', '')
        self.form['gender'] = request.POST.get('gender', '')
        self.form['college_id'] = request.POST.get('collegeId', 0)

    def form_to_model(self, obj):
        obj.id = self.form['id']
        obj.first_name = self.form['first_name']
        obj.last_name = self.form['last_name']
        obj.email = self.form['email']
        obj.mobile_no = self.form['mobile_no']
        obj.dob = self.form['dob']
        obj.gender = self.form['gender']
        obj.college_id = int(self.form['college_id'])
        obj.college_name = CollegeService().get(self.form['college_id']).name
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form['id'] = obj.id
        self.form['first_name'] = obj.first_name
        self.form['last_name'] = obj.last_name
        self.form['email'] = obj.email
        self.form['mobile_no'] = obj.mobile_no
        self.form['dob'] = obj.dob.strftime('%Y-%m-%d')
        self.form['gender'] = obj.gender
        self.form['college_id'] = obj.college_id
        self.form['college_name'] = obj.college_name

    def input_validation(self, request):
        input_error = self.form.get('input_error')
        input_error['error'] = False

        if DataValidator.is_null(self.form.get('first_name')):
            input_error['first_name'] = 'First Name is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('last_name')):
            input_error['last_name'] = 'Last Name is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('email')):
            input_error['email'] = 'Email is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('mobile_no')):
            input_error['mobile_no'] = 'Mobile No is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('dob')):
            input_error['dob'] = 'DOB is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('gender')) or request.POST.get('gender') == '0':
            input_error['gender'] = 'Gender is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get('college_id')) or request.POST.get('collegeId') == '0':
            input_error['college_id'] = 'College is required'
            input_error['error'] = True

        return input_error['error']

    def display(self, request, params={}):
        return render(request, self.get_template(), {'form': self.form, 'preload_data': self.preload(request)})

    def submit(self, request, params={}):
        try:
            student = self.form_to_model(Student())
            self.get_service().save(student)

            if self.form['id'] > 0:
                self.model_to_form(student)
                self.form['message'] = 'Student Updated Successfully...!!!'
            else:
                self.form['id'] = 0
                self.form['message'] = 'Student Added Successfully...!!!'

            self.form['error'] = False

        except Exception as e:
            self.form['message'] = str(e)
            self.form['error'] = True

        return render(request, self.get_template(), {'form': self.form, 'preload_data': self.preload(request)})

    def get_service(self):
        return StudentService()

    def get_template(self):
        return 'student.html'