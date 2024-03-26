from employees.models.models_addendum import Addendum
from employees.models.models_agreement import Agreement
from employees.models.models_payment import Payment
from employees.models.models_termination import Termination
from employees.models.models_vacation import Vacation
from rest_framework import serializers


class AddendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addendum
        fields = "__all__"


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        fields = "__all__"


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = "__all__"
