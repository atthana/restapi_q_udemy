from rest_framework import viewsets
from rest_framework.decorators import action
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
        # customers = Customer.objects.filter(
        #     id=3)  # พอเรามา override แบบนี้ มันก้อจะสนใจแค่ id=3 นะ แต่ไม่ทำ active=true ข้างบน
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args,
                 **kwargs):  # ใช้เมื่อมีการดึงค่า id ออกมา ถ้าพิมพ์ kwargs จะได้ {'pk': '2'} นะใน pdb
        obj = self.get_object()  # สร้าง object ขึั้นมา แล้วใส่เข้าไปให้เป็น serializer จิงๆเราทำเหมือนกับที่เราไป override มานะ
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
        # return Response({'details': 'Not allowed q'})  # คือ เราจะให้มัน return เป็นอะไรก็ได้นะ ผ่านทาง Response แบบนี้
        # return HttpResponseNotAllowed(
        #     'Q Not allowed')  # หรือจะส่งกลับไปแบบนี้ก้อได้ แบบที่ Django มีมาให้ อันนี้ได้ 405 นะ

    #  อันนี้แค่ไปก๊อบมาให้ดูว่า ที่เราไป override คือให้ไปทับกับตัวนี้นะ
    # class RetrieveModelMixin:
    #     """
    #     Retrieve a model instance.
    #     """
    #
    #     def retrieve(self, request, *args, **kwargs):
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance)
    #         return Response(serializer.data)

    def create(self, request, *args, **kwargs):  # อันนี้เป็นการทำ override create() บ้าง มันคือ POST method นะ
        data = request.data
        customer = Customer.objects.create(
            name=data['name'], address=data['address'], datasheet_id=data['datasheet']
        )
        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.profession.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):  # แบบนี้เทสด้วย PUT method ใน Postman นะ
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.datasheet_id = data['datasheet']

        profession = Profession.objects.get(id=data['profession'])

        customer.profession.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):  # อันนี้คือ PATCH method
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.datasheet_id = request.data.get('datasheet', customer.datasheet_id)

        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):  # อันนี้คือ DELETE method นะ
        customer = self.get_object()
        customer.delete()

        return Response({'detail': 'Object removed'})

    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    # การใช้ action แบบนี้เป็นการเพิ่ม urlให้มัน ตอนเรียกเราก้อแค่ GET ไปที่ http://localhost:8000/api/customers/3/deactivate/
    # จะทำให้ active กลายเป็น False ไปเลย คือ เป็ฯการ GET ที่เปลี่ยนค่าได้ หรือเรียกว่า custom actions

    @action(detail=False)
    def deactivate_all(self, request,
                       **kwargs):  # http://localhost:8000/api/customers/deactivate_all/ แค่นี้ก้อเป็น False หมดเลยทันที ไวมาก
        customers = Customer.objects.all()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request,
                     **kwargs):  # http://localhost:8000/api/customers/activate_all/ แค่ GET แบบนี้ก้อเป็น True หมดเลยทันที
        customers = Customer.objects.all()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])  # อันนี้ใช้ method POST  gเพื่อทำการเปลี่ยน status ของ active
    def change_status(self, request, **kwargs):  # http://localhost:8000/api/customers/change_status/ แต่ต้องใช้ POST method นะ
        status = True if request.data['active'] == 'True' else False

        customers = Customer.objects.all()
        customers.update(active=status)

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
