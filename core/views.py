from rest_framework import viewsets

from core.models import Customer
from core.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    # queryset = Customer.objects.filter(active=True)  # ถ้าเราต้องการ filter ก้อมาทำแบบนี้ได้เลย เพราะอันนี้คือการ query
    serializer_class = CustomerSerializer
