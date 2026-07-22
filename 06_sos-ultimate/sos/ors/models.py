from django.db import models


class DropdownItem:
    def get_key(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError


class User(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login_id = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, default='')
    role_id = models.IntegerField()
    role_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'sos_user'

class College(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = 'sos_college'

class Student(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    dob = models.DateField(max_length=20)
    gender = models.CharField(max_length=50, default='')
    college_id = models.IntegerField()
    college_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'sos_student'

class Role(DropdownItem, models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "sos_role"



class Course(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = 'sos_course'


class Faculty(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=20)
    college_id = models.IntegerField()
    college_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'sos_faculty'


class Subject(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = 'sos_subject'


class Marksheet(DropdownItem, models.Model):

    roll_no = models.CharField(max_length=50, unique=True)

    student_id = models.IntegerField(default=0)

    student_name = models.CharField(max_length=255)

    year = models.IntegerField()

    physics = models.IntegerField()

    chemistry = models.IntegerField()

    maths = models.IntegerField()

    def get_key(self):
        return self.id

    def get_value(self):
        return self.roll_no

    class Meta:
        db_table = "sos_marksheet"


class TimeTable(DropdownItem, models.Model):

    exam_date = models.DateField()

    exam_time = models.CharField(max_length=20)

    semester = models.CharField(max_length=20)

    course_id = models.IntegerField()

    course_name = models.CharField(max_length=100)

    subject_id = models.IntegerField()

    subject_name = models.CharField(max_length=100)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.exam_date.strftime("%d-%m-%Y")

    class Meta:
        db_table = "sos_timetable"
