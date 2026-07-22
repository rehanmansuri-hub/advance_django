from django.shortcuts import render

from .base_ctl import BaseCtl
from ors.models import Marksheet
from ors.service.marksheet_service import MarksheetService
from ors.utility.data_validator import DataValidator

from ..service.student_service import StudentService
from ..utility.html_utility import HtmlUtility


class MarksheetCtl(BaseCtl):

    def preload(self, request):
        student_list = StudentService().search({})

        preload_data = {}

        preload_data["student_select"] = HtmlUtility.get_list_from_beans(
            "student_id",
            int(self.form.get("student_id") or 0),
            student_list
        )

        return preload_data

    def request_to_form(self, request):
        self.form["id"] = int(request.POST.get("id") or 0)
        self.form["roll_no"] = request.POST.get("roll_no", "").strip()
        self.form["student_id"] = request.POST.get("student_id", 0)
        self.form["year"] = request.POST.get("year", "").strip()
        self.form["physics"] = request.POST.get("physics", "").strip()
        self.form["chemistry"] = request.POST.get("chemistry", "").strip()
        self.form["maths"] = request.POST.get("maths", "").strip()

    def form_to_model(self, obj):
        obj.id = self.form["id"]
        obj.roll_no = self.form["roll_no"]
        obj.year = self.form["year"]
        obj.physics = self.form["physics"]
        obj.chemistry = self.form["chemistry"]
        obj.maths = self.form["maths"]

        student_id = int(self.form.get("student_id") or 0)
        obj.student_id = student_id

        student = StudentService().get(student_id) if student_id > 0 else None

        print("Student ID =", student_id)
        print("Student =", student)

        if student:
            print("Student Name =", student.first_name)

        obj.student_name = student.first_name if student else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["roll_no"] = obj.roll_no
        self.form["student_id"] = obj.student_id
        self.form["year"] = obj.year
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths

    def input_validation(self, request):

        input_error = self.form.get("input_error")
        input_error["error"] = False

        # Roll No
        if DataValidator.is_null(self.form.get("roll_no")):
            input_error["roll_no"] = "Roll No is required"
            input_error["error"] = True

        # Student
        if DataValidator.is_null(self.form.get("student_id")) or self.form.get("student_id") == "0":
            input_error["student_id"] = "Student is required"
            input_error["error"] = True

        # Year
        if DataValidator.is_null(self.form.get("year")):
            input_error["year"] = "Year is required"
            input_error["error"] = True

        # Physics
        if DataValidator.is_null(self.form.get("physics")):
            input_error["physics"] = "Physics Marks is required"
            input_error["error"] = True
        else:
            try:
                physics = int(self.form.get("physics"))
                if physics < 0 or physics > 100:
                    input_error["physics"] = "Physics Marks must be between 0 and 100"
                    input_error["error"] = True
            except:
                input_error["physics"] = "Enter valid Physics Marks"
                input_error["error"] = True

        # Chemistry
        if DataValidator.is_null(self.form.get("chemistry")):
            input_error["chemistry"] = "Chemistry Marks is required"
            input_error["error"] = True
        else:
            try:
                chemistry = int(self.form.get("chemistry"))
                if chemistry < 0 or chemistry > 100:
                    input_error["chemistry"] = "Chemistry Marks must be between 0 and 100"
                    input_error["error"] = True
            except:
                input_error["chemistry"] = "Enter valid Chemistry Marks"
                input_error["error"] = True

        # Maths
        if DataValidator.is_null(self.form.get("maths")):
            input_error["maths"] = "Maths Marks is required"
            input_error["error"] = True
        else:
            try:
                maths = int(self.form.get("maths"))
                if maths < 0 or maths > 100:
                    input_error["maths"] = "Maths Marks must be between 0 and 100"
                    input_error["error"] = True
            except:
                input_error["maths"] = "Enter valid Maths Marks"
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

            marksheet = self.form_to_model(Marksheet())
            self.get_service().save(marksheet)

            self.model_to_form(marksheet)

            if self.form["id"] > 0:
                self.form["message"] = "Marksheet Updated Successfully...!!!"
            else:
                self.form["message"] = "Marksheet Added Successfully...!!!"

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
        return MarksheetService()

    def get_template(self):
        return "marksheet.html"