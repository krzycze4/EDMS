from companies.models import Address
from companies.serializers import AddressSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView


class AddressListAPIView(ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
