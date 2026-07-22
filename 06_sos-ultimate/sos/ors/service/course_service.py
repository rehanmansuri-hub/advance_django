from django.core.paginator import Paginator

from ors.models import Course
from ors.utility.data_validator import DataValidator


class CourseService:

    def save(self, obj):
        print('course service orm save()')
        duplicate = self.find_by_name(obj.name)

        if obj.id > 0:
            duplicate = duplicate.exclude(id=obj.id)

        if duplicate.exists():
            raise Exception('Name already exist')

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print('course service orm get()')
        try:
            return Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return None

    def delete(self, id):
        print('course service orm delete()')
        obj = self.get(id)
        if obj is not None:
            obj.delete()

    def find_by_name(self, name):
        print('course service orm find_by_name()')
        return Course.objects.filter(name=name)

    def search(self, params):
        print('course service orm search()')

        page_no = int(params.get('page_no', 1))
        page_size = int(params.get('page_size', 5))

        query = Course.objects.all()

        value = params.get('name', '')
        if DataValidator.is_not_null(value):
            query = query.filter(name__istartswith=value.strip())

        if page_size == 0:
            return query

        paginator = Paginator(query, page_size)
        page_obj = paginator.get_page(page_no)

        params['has_next'] = page_obj.has_next()
        params['has_previous'] = page_obj.has_previous()
        params['index'] = (page_no - 1) * page_size

        return page_obj
