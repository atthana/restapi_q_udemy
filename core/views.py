from core.models import Customer, Profession
from core.serializers import CustomerSerializer, ProfessionSerializer
from rest_framework import viewsets


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    # queryset = Customer.objects.filter(active=True)  # ถ้าเราต้องการ filter ก้อมาทำแบบนี้ได้เลย เพราะอันนี้คือการ query
    serializer_class = CustomerSerializer


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.filter(id=4)  # ถ้าแบบนี้ก้อจะช่วย filter จาก id ที่ 2 ได้เลยเวลาเรียก api 'professions'
    serializer_class = ProfessionSerializer
