from companies.api.serializers import ContactSerializer
from companies.models import Contact
from rest_framework.viewsets import ModelViewSet


class ContactModelViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
