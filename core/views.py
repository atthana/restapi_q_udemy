from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Customer, Profession, DataSheet, Document
from core.serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    # queryset = Customer.objects.filter(active=True)  # ถ้าเราต้องการ filter ก้อมาทำแบบนี้ได้เลย เพราะอันนี้คือการ query
    serializer_class = CustomerSerializer

    def get_queryset(
            self):  # คือ เรามา override method  ตรงนี้ได้เมื่อ queryset จะเป็นการ filter by active=True แทนได้ทั้งหมด
        active_customers = Customer.objects.filter(active=True)
        return active_customers

    def list(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        customers = Customer.objects.filter(id=3) # พอเรามา override แบบนี้ มันก้อจะสนใจแค่ id=3 นะ แต่ไม่ทำ active=true ข้างบน
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)



class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.filter(
        id=4)  # ถ้าแบบนี้ก้อจะช่วย filter จาก id ที่ 2 ได้เลยเวลาเรียก api 'professions'
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
