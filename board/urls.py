from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('sprints', views.SprintViewSet),
router.register('tasks', views.TaskViewSet),
router.register('users', views.UserViewSet),
