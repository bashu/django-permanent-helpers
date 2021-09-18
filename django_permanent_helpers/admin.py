# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.admin.utils import model_ngettext
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models.query_utils import Q
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django_permanent import settings as permanent_settings


def restore_selected(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    app_label = opts.app_label

    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    assert hasattr(queryset, "restore")

    if request.POST.get("post"):
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = str(obj)
                modeladmin.log_restore(request, obj, obj_display)
            for o in queryset:
                o.restore()
            modeladmin.message_user(
                request,
                _("Successfully restored %(count)d %(items)s.")
                % {"count": n, "items": model_ngettext(modeladmin.opts, n)},
                messages.SUCCESS,
            )
        # Return None to display the change list page again.
        return None

    objects_name = model_ngettext(queryset)

    context = {
        **modeladmin.admin_site.each_context(request),
        "title": _("Are you sure?"),
        "objects_name": str(objects_name),
        "queryset": queryset,
        "opts": opts,
        "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
        "media": modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(
        request,
        modeladmin.restore_selected_confirmation_template
        or [
            "admin/%s/%s/restore_selected_confirmation.html" % (app_label, opts.model_name),
            "admin/%s/restore_selected_confirmation.html" % app_label,
            "admin/restore_selected_confirmation.html",
        ],
        context,
    )


restore_selected.short_description = _("Restore selected %(verbose_name_plural)s")


class PermanentModelAdmin(admin.ModelAdmin):
    restore_selected_confirmation_template = "django_permanent_helpers/restore_selected_confirmation.html"
    actions = [restore_selected]

    def get_actions(self, request):
        actions = super(PermanentModelAdmin, self).get_actions(request)
        if "delete_selected" in actions:
            actions["delete_selected"] = (
                delete_selected,
                "delete_selected",
                _("Soft delete selected %(verbose_name_plural)s"),
            )
        return actions

    def log_restore(self, request, obj, object_repr):
        """
        Log that an object will be restored.
        The default implementation creates an admin LogEntry object.
        """
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(self.model).pk,
            object_id=obj.pk,
            object_repr=object_repr,
            action_flag=CHANGE,
        )

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
    title = _("deleted")
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (
            (1, _("Yes")),
            (0, _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(~Q(**{"%s__isnull" % permanent_settings.FIELD: int(self.value())})).distinct()
        return queryset
