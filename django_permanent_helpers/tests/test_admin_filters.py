from django.contrib import admin
from django.test import RequestFactory
from django.test import TestCase

from django_permanent_helpers.admin import PermanentModelListFilter

from .admin import MyPermanentModelAdmin
from .models import MyPermanentModel


class PermanentModelListFilterTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = MyPermanentModelAdmin(MyPermanentModel, admin.site)
        self.active = MyPermanentModel.objects.create(name="active")
        self.deleted = MyPermanentModel.objects.create(name="deleted")
        self.deleted.delete()

    def test_lookups(self):
        request = self.factory.get("/")
        f = PermanentModelListFilter(request, {}, MyPermanentModel, self.model_admin)
        assert f.lookups(request, self.model_admin) == ((1, "Yes"), (0, "No"))

    def test_queryset_no_value_is_noop(self):
        request = self.factory.get("/")
        f = PermanentModelListFilter(request, {}, MyPermanentModel, self.model_admin)
        assert set(f.queryset(request, MyPermanentModel.all_objects.all())) == {
            self.active,
            self.deleted,
        }

    def test_queryset_deleted_only(self):
        request = self.factory.get("/", {"deleted": "1"})
        f = PermanentModelListFilter(
            request,
            {"deleted": "1"},
            MyPermanentModel,
            self.model_admin,
        )
        qs = f.queryset(request, MyPermanentModel.all_objects.all())
        assert list(qs) == [self.deleted]
        assert self.active not in qs

    def test_queryset_non_deleted_only(self):
        request = self.factory.get("/", {"deleted": "0"})
        f = PermanentModelListFilter(
            request,
            {"deleted": "0"},
            MyPermanentModel,
            self.model_admin,
        )
        qs = f.queryset(request, MyPermanentModel.all_objects.all())
        assert list(qs) == [self.active]
        assert self.deleted not in qs
