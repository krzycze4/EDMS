from employees.models.models_addendum import Addendum
from employees.serializers import AddendumSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class AddendumListCreateAPIView(ListCreateAPIView):
    serializer_class = AddendumSerializer
    queryset = Addendum.objects.all()


class AddendumRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddendumSerializer
    queryset = Addendum.objects.all()
