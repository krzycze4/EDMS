from companies.api.serializers import ContactSerializer
from companies.models import Contact
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet


class ContactModelViewSet(ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
