from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления записями о платежах.
    Предоставляет полный набор операций CRUD (создание, чтение, обновление, удаление)
    для модели Payment."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']