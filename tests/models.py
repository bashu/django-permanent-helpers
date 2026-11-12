# ruff: noqa: DJ001
from django.db import models
from django.db.models import Model

from django_permanent.managers import MultiPassThroughManager
from django_permanent.models import PermanentModel
from django_permanent.query import DeletedQuerySet
from django_permanent.query import NonDeletedQuerySet
from django_permanent.query import PermanentQuerySet


class BaseTestModel(Model):
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)


class MyPermanentModel(PermanentModel, BaseTestModel):
    name = models.CharField(max_length=255, blank=True, null=True)


class RegularModel(BaseTestModel):
    name = models.CharField(max_length=255, blank=True, null=True)


class RemovableRegularDepended(PermanentModel, BaseTestModel):
    dependence = models.ForeignKey(
        RegularModel,
        on_delete=models.SET_NULL,
        null=True,
    )


class RemovableDepended(BaseTestModel):
    dependence = models.ForeignKey(MyPermanentModel, on_delete=models.CASCADE)


class NonRemovableDepended(PermanentModel, BaseTestModel):
    dependence = models.ForeignKey(
        MyPermanentModel,
        on_delete=models.DO_NOTHING,
    )


class NonRemovableNullableDepended(PermanentModel, BaseTestModel):
    dependence = models.ForeignKey(
        MyPermanentModel,
        on_delete=models.SET_NULL,
        null=True,
    )


class RemovableNullableDepended(PermanentModel, BaseTestModel):
    dependence = models.ForeignKey(
        MyPermanentModel,
        on_delete=models.SET_NULL,
        null=True,
    )


class PermanentDepended(PermanentModel, BaseTestModel):
    dependence = models.ForeignKey(MyPermanentModel, on_delete=models.CASCADE)


class M2MFrom(BaseTestModel):
    pass


class PermanentM2MThrough(PermanentModel):
    m2m_from = models.ForeignKey(
        "M2MFrom",
        on_delete=models.SET_NULL,
        null=True,
    )
    m2m_to = models.ForeignKey(
        "M2MTo",
        on_delete=models.SET_NULL,
        null=True,
    )


class M2MTo(BaseTestModel):
    m2m_from = models.ManyToManyField("M2MFrom", through=PermanentM2MThrough)


class MyPermanentQuerySet(PermanentQuerySet):
    def test(self):
        pass


class MyPermanentModelWithManager(PermanentModel, BaseTestModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    objects = MultiPassThroughManager(
        MyPermanentQuerySet,
        NonDeletedQuerySet,
    )
    deleted_objects = MultiPassThroughManager(
        MyPermanentQuerySet,
        DeletedQuerySet,
    )
    any_objects = MultiPassThroughManager(
        MyPermanentQuerySet,
        PermanentQuerySet,
    )


class TestQS:
    def test(self):
        return "ok"


class CustomQsPermanent(PermanentModel, BaseTestModel):
    objects = MultiPassThroughManager(TestQS, DeletedQuerySet)


class RestoreOnCreateModel(PermanentModel, BaseTestModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Permanent:
        restore_on_create = True


class LazyReferencePermanent(PermanentModel, BaseTestModel):
    """Test model with lazy reference (string) - valid configuration."""

    # Lazy reference to another PermanentModel - OK!
    permanent = models.ForeignKey(
        "MyPermanentModel",
        on_delete=models.CASCADE,
    )
    # Lazy reference to RegularModel with SET_NULL - also OK!
    regular = models.ForeignKey(
        "RegularModel",
        on_delete=models.SET_NULL,
        null=True,
    )
