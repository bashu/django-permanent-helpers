from django.contrib import admin

from django_permanent_helpers.admin import PermanentModelAdmin
from django_permanent_helpers.admin import PermanentModelListFilter

from .models import MyPermanentModel
from .models import RegularModel


@admin.register(MyPermanentModel)
class MyPermanentModelAdmin(PermanentModelAdmin):
    list_filter = (PermanentModelListFilter,)


# Registered with the plain admin to exercise the get_queryset() fallback
# branch for models that don't have an `all_objects` manager.
admin.site.register(RegularModel, PermanentModelAdmin)
