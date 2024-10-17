"""URL routing for the parent application."""

from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'users'

router = DefaultRouter()
router.register('membership', TeamMembershipViewSet)
router.register('teams', TeamViewSet)
router.register('users', UserViewSet)

urlpatterns = router.urls
