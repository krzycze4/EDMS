from companies.models import Address, Company, Contact
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def validate(self, attrs):
        if Address.objects.filter(
            street_name=attrs["street_name"],
            street_number=attrs["street_number"],
            city=attrs["city"],
            postcode=attrs["postcode"],
            country=attrs["country"],
        ).exists():
            raise serializers.ValidationError("Address has already existed in database.")
        else:
            return attrs


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

    def validate(self, attrs):
        if Contact.objects.filter(
            name=attrs["name"],
            email=attrs["email"],
            phone=attrs["phone"],
            company=attrs["company"],
        ).exists():
            raise serializers.ValidationError("Contact has already existed in database.")
        else:
            return attrs
