from django.core.paginator import Paginator

from ors.models import TimeTable
from ors.utility.data_validator import DataValidator


class TimeTableService:

    def save(self, obj):
        print("TimeTable Service ORM Save()")

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print("TimeTable Service ORM Get()")
        try:
            return TimeTable.objects.get(id=pk)
        except TimeTable.DoesNotExist:
            return None

    def delete(self, pk):
        print("TimeTable Service ORM Delete()")
        obj = self.get(pk)
        if obj:
            obj.delete()

    def search(self, params):
        print("TimeTable Service ORM Search()")

        page_no = int(params.get("page_no", 1))
        page_size = int(params.get("page_size", 5))

        query = TimeTable.objects.all()

        semester = params.get("semester", "")
        if DataValidator.is_not_null(semester):
            query = query.filter(semester__istartswith=semester.strip())

        if page_size == 0:
            return query

        paginator = Paginator(query, page_size)
        page = paginator.get_page(page_no)

        params["has_next"] = page.has_next()
        params["has_previous"] = page.has_previous()
        params["index"] = (page_no - 1) * page_size

        return page