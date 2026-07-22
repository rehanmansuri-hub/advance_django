from django.core.paginator import Paginator

from ors.models import Subject
from ors.utility.data_validator import DataValidator
class SubjectService:

    def save(self, obj):
        print("Subject Service ORM Save()")

        duplicate = self.find_by_name(obj.name)

        if obj.id > 0:
            duplicate = duplicate.exclude(id=obj.id)

        if duplicate.exists():
            raise Exception("Subject Name already exists")

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print("Subject Service ORM Get()")
        try:
            return Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            return None

    def delete(self, pk):
        print("Subject Service ORM Delete()")
        obj = self.get(pk)
        if obj:
            obj.delete()

    def find_by_name(self, name):
        print("Subject Service ORM Find By Name()")
        return Subject.objects.filter(name=name)

    def search(self, params):
        print("Subject Service ORM Search()")

        page_no = int(params.get("page_no", 1))
        page_size = int(params.get("page_size", 5))

        query = Subject.objects.all()

        name = params.get("name", "")
        if DataValidator.is_not_null(name):
            query = query.filter(name__istartswith=name.strip())

        if page_size == 0:
            return query

        paginator = Paginator(query, page_size)
        page = paginator.get_page(page_no)

        params["has_next"] = page.has_next()
        params["has_previous"] = page.has_previous()
        params["index"] = (page_no - 1) * page_size

        return page