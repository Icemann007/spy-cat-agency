from django.urls import include, path
from rest_framework import routers

from missions.views import MissionViewSet

router = routers.DefaultRouter()

router.register(r"", MissionViewSet, basename="mission")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "missions"
