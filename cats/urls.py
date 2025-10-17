from django.urls import include, path
from rest_framework import routers

from cats.views import CatViewSet

router = routers.DefaultRouter()

router.register(r"", CatViewSet, basename="сat")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "cats"
