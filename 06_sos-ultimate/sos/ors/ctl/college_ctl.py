from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.utility.data_validator import DataValidator
from ors.models import College
from ors.service.college_service import CollegeService


class CollegeCtl(BaseCtl):
    def request_to_form(self, request):

        form_id = request.POST.get('id')
        self.form['id'] = '' if form_id in (None, '', '0') else form_id
        self.form['name'] = request.POST.get('name')
        self.form['address'] = request.POST.get('address')
        self.form['state'] = request.POST.get('state')
        self.form['city'] = request.POST.get('city')
        self.form['phoneNumber'] = request.POST.get('phoneNumber')

    def form_to_model(self, obj):

        pk = int(self.form['id']) if self.form['id'] else 0

        obj.id = pk
        obj.name = self.form['name']
        obj.address = self.form['address']
        obj.state = self.form['state']
        obj.city = self.form['city']
        obj.phoneNumber = self.form['phoneNumber']

        return obj

    def model_to_form(self, obj):

        if obj is None:
            return

        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['address'] = obj.address
        self.form['state'] = obj.state
        self.form['city'] = obj.city
        self.form['phoneNumber'] = obj.phoneNumber

    def input_validation(self, request):

        input_error = self.form.get("input_error")
        input_error['error'] = False

        if DataValidator.is_null(self.form.get("name")):
            input_error['name'] = 'Name is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get("address")):
            input_error['address'] = 'Address is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get("state")):
            input_error['state'] = 'State is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get("city")):
            input_error['city'] = 'City is required'
            input_error['error'] = True

        if DataValidator.is_null(self.form.get("phoneNumber")):
            input_error['phoneNumber'] = 'Phone Number is required'
            input_error['error'] = True

        return input_error['error']

    def display(self, request, params={}):

        return render(
            request,
            self.get_template(),
            {'form': self.form, "preload_data": self.preload(request)})

    def submit(self, request, params={}):

        try:

            college = self.form_to_model(College())

            self.get_service().save(college)

            # UPDATE CASE
            if request.POST.get('operation') == 'update':

                self.model_to_form(college)

                self.form['message'] = 'College Updated Successfully...!!!'

            # SAVE CASE
            else:

                self.model_to_form(college)

                # Add mode me rakhne ke liye id clear
                self.form['id'] = ''

                self.form['message'] = 'College Added Successfully...!!!'

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

        return CollegeService()

    def get_template(self):

        return 'college.html'
