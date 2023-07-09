from . import models, serializers, mixins, forms
from django.contrib.auth import get_user_model
from rest_framework import viewsets

User = get_user_model()


class SprintViewSet(mixins.DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""

    queryset = models.Sprint.objects.order_by('end')
    serializer_class = serializers.SprintSerializer
    filter_class = forms.SprintFilter
    search_fields = ('name',)
    ordering_fields = ('end', 'name',)


class TaskViewSet(mixins.DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating tasks."""

    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    filter_class = forms.TaskFilter
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed',)


class UserViewSet(mixins.DefaultMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = serializers.UserSerializer
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    search_fields = (User.USERNAME_FIELD,)