from  . import models
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from datetime import date 
from django.utils.translation import gettext_lazy as _

User = get_user_model() 


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField(method_name='get_links')
    # active = serializers.BooleanField(source='is_active')

    class Meta:
        model = User 
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, object):
        request = self.context['request']
        username = object.get_username()

        return {
            'self': reverse(
                viewname='user-detail',
                kwargs={
                    User.USERNAME_FIELD: username
                },
                request=request
            ),
            'tasks': f"{reverse(viewname='task-list', request=request)}?assigned={username}"
        }


class SprintSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(method_name='get_links')

    class Meta:
        model = models.Sprint 
        fields = ('id', 'name', 'description', 'end', 'links')

    def get_links(self, object):
        request = self.context['request']

        return {
            'self': reverse(
                viewname='sprint-detail',
                kwargs={
                    'pk': object.pk
                },
                request=request
            ),
            'tasks': reverse(
                viewname='task-list',
                request=request,
            ) + f'?sprint={object.pk}',
        }

    def validate_end(self, value):
        new = self.instance is None
        changed = self.instance and self.instance.end != value

        if (new or changed) and (value < date.today()):
            message = _('End date cannot be in the past.')
            raise serializers.ValidationError(message)
        return value


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(
        slug_field = User.USERNAME_FIELD,
        required = False,
        allow_null = True,
        queryset = User.objects.all()
    )
    status_display = serializers.SerializerMethodField(method_name='get_status_display')
    links = serializers.SerializerMethodField(method_name='get_links')

    class Meta:
        model = models.Task 
        fields = (
            'id', 'name', 'description', 'sprint', 'status', 'status_display',
            'order', 'assigned', 'started', 'due', 'completed', 'links'
        )

    def get_status_display(self, object):
        return object.get_status_display()

    def get_links(self, object):
        request = self.context['request']

        links = {
            'self': reverse(
                viewname='task-detail',
                kwargs={
                    'pk': object.pk
                },
                request=request
            ),
            'sprint': None,
            'assigned': None,
        }

        if object.sprint_id:
            links['sprint'] = reverse(
                viewname='sprint-detail',
                kwargs = {
                    'pk': object.sprint_id
                },
                request=request
            )
        
        if object.assigned:
            links['assigned'] = reverse(
                viewname='user-detail',
                kwargs = {
                    User.USERNAME_FIELD: object.assigned
                },
                request=request
            )
        
        return links

    def validate_sprint(self, value):
        if self.instance and self.instance.pk:
            if value != self.instance.sprint:
                if self.instance.status == models.Task.STATUS_DONE:
                    message = _('Cannot change the sprint of a completed task.')
                    raise serializers.ValidationError(message)
            if value and value.end < date.today():
                message = _('Cannot assign tasks to past sprints')
                raise serializers.ValidationError(message)
        else:
            if value and value.end < date.today():
                message = _('Cannot add tasks to past sprints.')
                raise serializers.ValidationError(message)
        
        return value 

    def validate(self, attrs):
        sprint = attrs.get('sprint')
        status = attrs.get('status', models.Task.STATUS_TODO)
        started = attrs.get('started')
        completed = attrs.get('completed')

        if not sprint and status != models.Task.STATUS_TODO:
            message = _('Backlog tasks must have "Not Started" status.')
            raise serializers.ValidationError(message)
        
        if started and status == models.Task.STATUS_TODO:
            message = _('Started date cannot be set for not started tasks.')
            raise serializers.ValidationError(message)

        if completed and status != models.Task.STATUS_DONE:
            message = _('Completed date cannot be set for uncompleted tasks.')
            raise serializers.ValidationError(message)
        
        return attrs
