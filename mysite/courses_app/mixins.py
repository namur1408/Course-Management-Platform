from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from .models import ActionLog
from django.utils.timezone import now
from django.urls import reverse_lazy

class CreatorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != request.user:
            raise PermissionDenied("You are not the creator of this object.")
        return super().dispatch(request, *args, **kwargs)

class LogActionMixin:
    action_type = None
    def log_action(self, obj):
        ActionLog.objects.create(
            user=self.request.user,
            action_type=self.action_type,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        )

class FormCreatorAssignMixin:
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Admins only.")
        return super().dispatch(request, *args, **kwargs)

class OwnerOrPermissionMixin:
    owner_field = 'creator'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner = getattr(obj, getattr(self, 'owner_field', 'creator'))
        if owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        if self.permission_required and request.user.has_perm(self.permission_required):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Not allowed.")

class AdditionalFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UpdateTimestampMixin:
    def form_valid(self, form):
        if hasattr(form.instance, "updated_at"):
            form.instance.updated_at = now()
        return super().form_valid(form)

class SuccessUrlMixin:
    related_field = None

    def get_success_url(self):
        related_obj = getattr(self.object, self.related_field)
        return reverse_lazy(f'{related_obj._meta.model_name}_detail', kwargs={'pk': related_obj.pk})
