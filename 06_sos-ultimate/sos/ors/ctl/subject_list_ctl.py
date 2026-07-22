from django.shortcuts import render
from .base_ctl import BaseCtl
from ors.service.subject_service import SubjectService

class SubjectListCtl(BaseCtl):

    def request_to_form(self, request):
        self.form['name'] = request.POST.get('name', '').strip()
        self.form['page_no'] = request.POST.get('pageNo', 1)
        self.form['page_size'] = 5

    def display(self, request, params={}):
        self.form['page_no'] = 1
        self.form['page_size'] = 5

        subject_list = self.get_service().search(self.form)
        self.form['list'] = subject_list

        return render(request, self.get_template(), {'form': self.form})

    def submit(self, request, params={}):
        self.request_to_form(request)

        if request.POST.get('operation', '') == 'next':
            self.form['page_no'] = int(request.POST['pageNo']) + 1

        if request.POST.get('operation', '') == 'previous':
            self.form['page_no'] = int(request.POST['pageNo']) - 1

        if request.POST.get('operation', '') == 'search':
            self.form['page_no'] = 1

        subject_list = self.get_service().search(self.form)
        self.form['list'] = subject_list

        return render(request, self.get_template(), {'form': self.form})

    def get_service(self):
        return SubjectService()

    def get_template(self):
        return 'subjectlist.html'
