from django.core.paginator import Paginator

from ors.models import Faculty
from ors.utility.data_validator import DataValidator


class FacultyService:

    def save(self, obj):
        print('faculty service orm save()')
        duplicate = self.find_by_email(obj.email)

        if obj.id > 0:
            duplicate = duplicate.exclude(id=obj.id)

        if duplicate.exists():
            raise Exception('Email already exist')

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print('faculty service orm get()')
        try:
            return Faculty.objects.get(id=pk)
        except Faculty.DoesNotExist:
            return None

    def delete(self, id):
        print('faculty service orm delete()')
        obj = self.get(id)
        if obj is not None:
            obj.delete()

    def find_by_email(self, email):
        print('faculty service orm find_by_email()')
        return Faculty.objects.filter(email=email)

    def search(self, params):
        print('faculty service orm search()')

        page_no = int(params.get('page_no', 1))
        page_size = int(params.get('page_size', 5))

        query = Faculty.objects.all()

        value = params.get('first_name', '')
        if DataValidator.is_not_null(value):
            query = query.filter(first_name__istartswith=value.strip())

        college_id = params.get('college_id', 0)
        if str(college_id).isdigit() and int(college_id) > 0:
            query = query.filter(college_id=int(college_id))

        if page_size == 0:
            return query

        paginator = Paginator(query, page_size)
        page_obj = paginator.get_page(page_no)

        params['has_next'] = page_obj.has_next()
        params['has_previous'] = page_obj.has_previous()
        params['index'] = (page_no - 1) * page_size

        return page_obj
