from rest_framework import viewsets

from cats.models import Cat
from cats.serializers import CatSerializer, CatSalaryUpdateSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return CatSalaryUpdateSerializer

        return CatSerializer
