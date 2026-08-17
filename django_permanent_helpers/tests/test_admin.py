from http import HTTPStatus

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.models import CHANGE
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from django_permanent_helpers.admin import PermanentModelAdmin
from django_permanent_helpers.admin import restore_selected

from .admin import MyPermanentModelAdmin
from .models import MyPermanentModel
from .models import RegularModel

CHANGELIST_URL = "admin:tests_mypermanentmodel_changelist"


class PermanentModelAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.active = MyPermanentModel.objects.create(name="active")
        self.deleted = MyPermanentModel.objects.create(name="deleted")
        self.deleted.delete()
        self.regular = RegularModel.objects.create(name="regular")
        self.model_admin = MyPermanentModelAdmin(MyPermanentModel, admin.site)
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )

    def test_all_objects(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        assert set(self.model_admin.get_queryset(request)) == {
            self.active,
            self.deleted,
        }

    def test_default_manager(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        assert list(
            PermanentModelAdmin(RegularModel, admin.site).get_queryset(request),
        ) == [self.regular]

    def test_ordering(self):
        request = self.factory.get("/")
        request.user = self.admin_user

        class OrderedAdmin(MyPermanentModelAdmin):
            ordering = ("name",)

        model_admin = OrderedAdmin(MyPermanentModel, admin.site)
        assert list(model_admin.get_queryset(request)) == [self.active, self.deleted]


class DeleteSelectedTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = MyPermanentModelAdmin(MyPermanentModel, admin.site)
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )

    def test_delete_selected(self):
        request = self.factory.get("/")
        request.user = self.admin_user
        actions = self.model_admin.get_actions(request)
        func, name, description = actions["delete_selected"]
        assert func is delete_selected
        assert name == "delete_selected"
        assert description == "Soft delete selected %(verbose_name_plural)s"


class RestoreSelectedTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.permanent = MyPermanentModel.objects.create(name="obj")
        self.permanent.delete()
        self.model_admin = MyPermanentModelAdmin(MyPermanentModel, admin.site)
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pw",  # noqa: S106
        )
        self.client.force_login(self.admin_user)

    def test_confirmation(self):
        response = self.client.post(
            reverse(CHANGELIST_URL),
            {
                "action": "restore_selected",
                helpers.ACTION_CHECKBOX_NAME: [str(self.permanent.pk)],
            },
        )
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(
            response,
            "django_permanent_helpers/restore_selected_confirmation.html",
        )
        self.assertContains(response, f'value="{self.permanent.pk}"')

    def test_permission(self):
        user = get_user_model().objects.create_user(
            username="staff",
            password="pw",  # noqa: S106
            is_staff=True,
        )
        content_type = ContentType.objects.get_for_model(MyPermanentModel)
        user.user_permissions.add(
            Permission.objects.get(
                content_type=content_type,
                codename="view_mypermanentmodel",
            ),
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse(CHANGELIST_URL),
            {
                "action": "restore_selected",
                helpers.ACTION_CHECKBOX_NAME: [str(self.permanent.pk)],
            },
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_restore_selected(self):
        assert not MyPermanentModel.objects.filter(pk=self.permanent.pk).exists()

        response = self.client.post(
            reverse(CHANGELIST_URL),
            {
                "action": "restore_selected",
                helpers.ACTION_CHECKBOX_NAME: [str(self.permanent.pk)],
                "post": "yes",
            },
        )
        self.assertRedirects(response, reverse(CHANGELIST_URL))

        restored = MyPermanentModel.all_objects.get(pk=self.permanent.pk)
        assert restored.removed is None

        log_entry = LogEntry.objects.get(
            object_id=str(self.permanent.pk),
            content_type=ContentType.objects.get_for_model(MyPermanentModel),
        )
        assert log_entry.action_flag == CHANGE
        assert log_entry.user_id == self.admin_user.pk

        messages = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("Successfully restored" in m for m in messages)

    def test_empty_queryset_is_noop(self):
        request = self.factory.post("/", {"post": "yes"})
        request.user = self.admin_user
        result = restore_selected(
            self.model_admin,
            request,
            MyPermanentModel.objects.none(),
        )
        assert result is None
        assert LogEntry.objects.count() == 0
