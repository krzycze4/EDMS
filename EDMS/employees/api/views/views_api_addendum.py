from employees.api.serializers import AddendumSerializer
from employees.models.models_addendum import Addendum
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class AddendumModelViewSet(ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddendumSerializer
    queryset = Addendum.objects.all()
