from employees.api.serializers import AddendumSerializer
from employees.models.models_addendum import Addendum
from rest_framework.viewsets import ModelViewSet


class AddendumModelViewSet(ModelViewSet):
    serializer_class = AddendumSerializer
    queryset = Addendum.objects.all()
