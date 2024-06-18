from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.api.serializers import UserSerializer

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions

User = get_user_model()


class UserModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
