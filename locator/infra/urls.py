from django.urls import path, include
from rest_framework.routers import DefaultRouter
from locator.presenters.views import LocatorViewSet

router = DefaultRouter(trailing_slash=False)
router.register("", LocatorViewSet, basename="api")

app_name = "locator"

urlpatterns = [
    path("", include(router.urls)),
]
