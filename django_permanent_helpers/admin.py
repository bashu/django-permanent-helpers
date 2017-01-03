# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.db.models.query_utils import Q
from django.core.exceptions import PermissionDenied
from django.contrib.admin.utils import model_ngettext
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.actions import delete_selected

from django_permanent import settings as permanent_settings

delete_selected.short_description = _("Soft delete selected %(verbose_name_plural)s")


def restore_selected(modeladmin, request, queryset):
    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    n = queryset.count()
    if n:
        queryset.restore()
        modeladmin.message_user(request, _("Successfully restored %(count)d %(items)s.") % {
            "count": n, "items": model_ngettext(modeladmin.opts, n)
        }, messages.SUCCESS)
    # Return None to display the change list page again.
    return None

restore_selected.short_description = _("Restore selected %(verbose_name_plural)s")


class PermanentModelAdmin(admin.ModelAdmin):
    actions = [delete_selected, restore_selected]

    def get_queryset(self, request):
        try:
            qs = self.model.all_objects.all()
        except Exception as ex:
            qs = self.model._default_manager.all()

        ordering = self.get_ordering(request) or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class PermanentModelListFilter(admin.SimpleListFilter):
    title = _('deleted')
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (
            (1, _('Yes')),
            (0, _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(~Q(**{'%s__isnull' % permanent_settings.FIELD: int(self.value())})).distinct()
        return queryset

