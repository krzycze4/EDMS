from employees.models.models_agreement import Agreement
from employees.serializers import AgreementSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class AgreementListCreateAPIView(ListCreateAPIView):
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()


class AgreementRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
