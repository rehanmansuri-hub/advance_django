from django.core.paginator import Paginator

from ors.models import Marksheet
from ors.utility.data_validator import DataValidator


class MarksheetService:

    def save(self, obj):
        print("Marksheet Service ORM Save()")

        duplicate = self.find_by_roll_no(obj.roll_no)

        if obj.id > 0:
            duplicate = duplicate.exclude(id=obj.id)

        if duplicate.exists():
            raise Exception("Roll No already exists")

        if obj.id == 0:
            obj.id = None

        obj.save()

    def get(self, pk):
        print("Marksheet Service ORM Get()")
        try:
            return Marksheet.objects.get(id=pk)
        except Marksheet.DoesNotExist:
            return None

    def delete(self, pk):
        print("Marksheet Service ORM Delete()")
        obj = self.get(pk)
        if obj:
            obj.delete()

    def find_by_roll_no(self, roll_no):
        print("Marksheet Service ORM Find By Roll No()")
        return Marksheet.objects.filter(roll_no=roll_no)

    def search(self, params):
        print("Marksheet Service ORM Search()")

        page_no = int(params.get("page_no", 1))
        page_size = int(params.get("page_size", 5))

        query = Marksheet.objects.all()

        roll_no = params.get("roll_no", "")
        if DataValidator.is_not_null(roll_no):
            query = query.filter(roll_no__istartswith=roll_no.strip())

        if page_size == 0:
            return query

        paginator = Paginator(query, page_size)
        page = paginator.get_page(page_no)

        params["has_next"] = page.has_next()
        params["has_previous"] = page.has_previous()
        params["index"] = (page_no - 1) * page_size

        return page