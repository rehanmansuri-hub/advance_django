from django.core.paginator import Paginator

from ors.models import Student
from ors.utility.data_validator import DataValidator


class StudentService:

    def save(self, obj):
        print('student service orm save()')
        duplicate = self.find_by_email(obj.email)

        if obj.id > 0:
            duplicate = duplicate.exclude(id=obj.id)

        if duplicate.exists():
            raise Exception('Email already exist')

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print('student service orm get()')
        try:
            return Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return None

    def delete(self, id):
        print('student service orm delete()')
        obj = self.get(id)
        if obj is not None:
            obj.delete()

    def find_by_email(self, email):
        print('student service orm find_by_email()')
        return Student.objects.filter(email=email)

    def search(self, params):
        print('student service orm search()')

        page_no = int(params.get('page_no', 1))
        page_size = int(params.get('page_size', 5))

        query = Student.objects.all()

        value = params.get('first_name', '')
        if DataValidator.is_not_null(value):
            query = query.filter(first_name__istartswith=value.strip())

        college_id = params.get('college_id', 0)
        if str(college_id).isdigit() and int(college_id) > 0:
            query = query.filter(college_id=int(college_id))

        paginator = Paginator(query, page_size)
        page_obj = paginator.get_page(page_no)

        params['has_next'] = page_obj.has_next()
        params['has_previous'] = page_obj.has_previous()
        params['index'] = (page_no - 1) * page_size

        return page_obj