from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.service.college_service import CollegeService
from ors.service.faculty_service import FacultyService
from ors.utility.html_utility import HtmlUtility


class FacultyListCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({'page_size': 0})
        self.form['preload_data']['college_select'] = HtmlUtility.get_list_from_beans(
            'collegeId',
            int(self.form.get('college_id') or 0),
            college_list
        )

    def request_to_form(self, request):
        self.form['first_name'] = request.POST.get('firstName', '').strip()
        self.form['college_id'] = request.POST.get('collegeId', 0)
        self.form['page_no'] = request.POST.get('pageNo', 1)
        self.form['page_size'] = 5

    def display(self, request, params={}):
        self.form['page_no'] = 1
        self.form['page_size'] = 5

        faculty_list = self.get_service().search(self.form)
        self.form['list'] = faculty_list

        return render(request, self.get_template(), {'form': self.form, 'preload_data': self.preload(request)})

    def submit(self, request, params={}):
        self.request_to_form(request)

        if request.POST.get('operation', '') == 'next':
            self.form['page_no'] = int(request.POST['pageNo']) + 1

        if request.POST.get('operation', '') == 'previous':
            self.form['page_no'] = int(request.POST['pageNo']) - 1

        if request.POST.get('operation', '') == 'search':
            self.form['page_no'] = 1

        faculty_list = self.get_service().search(self.form)
        self.form['list'] = faculty_list

        return render(request, self.get_template(), {'form': self.form, 'preload_data': self.preload(request)})

    def get_service(self):
        return FacultyService()

    def get_template(self):
        return 'facultylist.html'
