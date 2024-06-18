from companies.api.serializers import ContactSerializer
from companies.models import Contact
from rest_framework.viewsets import ModelViewSet

from EDMS.custom_django_model_permissions import CustomDjangoModelPermissions


class ContactModelViewSet(ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
