from companies.models import Contact
from companies.serializers import ContactSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ContactListCreateAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ContactRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
