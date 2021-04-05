from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from core.models import Customer, Profession, DataSheet, Document
from core.serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.all()
    # queryset = Customer.objects.filter(active=True)  # ถ้าเราต้องการ filter ก้อมาทำแบบนี้ได้เลย เพราะอันนี้คือการ query
    serializer_class = CustomerSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    filterset_fields = ('name',)
    search_fields = ('name', 'address')
    # ordering_fields = '__all__'
    ordering = ('id',)
    # lookup_field = 'name'
    authentication_classes = [
        TokenAuthentication, ]  # บรรทัดนี้ใช้เพื่อทำให้ api viewset อันนี้ต้องใช้ token เข้ามานะ ไม่สามารถ get ได้แบบปกติแล้ว

    def get_queryset(
            self):  # แบบนี้ปกติจะ get ได้หมด หรือจะส่ง address='xx' เข้ามา filter ก็ได้ localhost:8000/api/customers/?address='form'
        address = self.request.query_params.get('address', None)

        # import pdb
        # pdb.set_trace()

        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True
        if address:
            customers = Customer.objects.filter(address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)
        return customers

    # def get_queryset(self):  # ผมเทสผ่านล่ะนะ แต่ถ้าจะเทส ก้อไป comment method อื่นออก
    #     # import pdb;
    #     # pdb.set_trace()
    #
    #     id = self.request.query_params.get('id', None)
    #     status = True if self.request.query_params['active'] == 'True' else False
    #
    #     if id:
    #         customers = Customer.objects.filter(id=id, active=status)
    #     else:
    #         customers = Customer.objects.filter(active=status)
    #     return customers
    #
    # # def get_queryset(
    # #         self):  # คือ เรามา override method  ตรงนี้ได้เมื่อ queryset จะเป็นการ filter by active=True แทนได้ทั้งหมด
    # #     active_customers = Customer.objects.filter(active=True)
    # #     return active_customers
    #
    # def list(self, request, *args, **kwargs):
    #     # import pdb
    #     # pdb.set_trace()
    #     # customers = Customer.objects.filter(
    #     #     id=3)  # พอเรามา override แบบนี้ มันก้อจะสนใจแค่ id=3 นะ แต่ไม่ทำ active=true ข้างบน
    #     customers = self.get_object()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, *args,
    #              **kwargs):  # ใช้เมื่อมีการดึงค่า id ออกมา ถ้าพิมพ์ kwargs จะได้ {'pk': '2'} นะใน pdb
    #     obj = self.get_object()  # สร้าง object ขึั้นมา แล้วใส่เข้าไปให้เป็น serializer จิงๆเราทำเหมือนกับที่เราไป override มานะ
    #     serializer = CustomerSerializer(obj)
    #     return Response(serializer.data)
    #     # return Response({'details': 'Not allowed q'})  # คือ เราจะให้มัน return เป็นอะไรก็ได้นะ ผ่านทาง Response แบบนี้
    #     # return HttpResponseNotAllowed(
    #     #     'Q Not allowed')  # หรือจะส่งกลับไปแบบนี้ก้อได้ แบบที่ Django มีมาให้ อันนี้ได้ 405 นะ
    #
    # #  อันนี้แค่ไปก๊อบมาให้ดูว่า ที่เราไป override คือให้ไปทับกับตัวนี้นะ
    # # class RetrieveModelMixin:
    # #     """
    # #     Retrieve a model instance.
    # #     """
    # #
    # #     def retrieve(self, request, *args, **kwargs):
    # #         instance = self.get_object()
    # #         serializer = self.get_serializer(instance)
    # #         return Response(serializer.data)
    #
    # def create(self, request, *args, **kwargs):  # อันนี้เป็นการทำ override create() บ้าง มันคือ POST method นะ
    #     data = request.data
    #     customer = Customer.objects.create(
    #         name=data['name'], address=data['address'], datasheet_id=data['datasheet']
    #     )
    #     profession = Profession.objects.get(id=data['profession'])
    #
    #     for p in customer.professions.all():
    #         customer.professions.remove(p)
    #
    #     customer.profession.add(profession)
    #     customer.save()
    #
    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):  # แบบนี้เทสด้วย PUT method ใน Postman นะ
    #     customer = self.get_object()
    #     data = request.data
    #     customer.name = data['name']
    #     customer.address = data['address']
    #     customer.datasheet_id = data['datasheet']
    #
    #     profession = Profession.objects.get(id=data['profession'])
    #
    #     customer.profession.add(profession)
    #     customer.save()
    #
    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, *args, **kwargs):  # อันนี้คือ PATCH method
    #     customer = self.get_object()
    #     customer.name = request.data.get('name', customer.name)
    #     customer.address = request.data.get('address', customer.address)
    #     customer.datasheet_id = request.data.get('datasheet', customer.datasheet_id)
    #
    #     customer.save()
    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, *args, **kwargs):  # อันนี้คือ DELETE method นะ
    #     customer = self.get_object()
    #     customer.delete()
    #
    #     return Response({'detail': 'Object removed'})
    #
    # @action(detail=True)
    # def deactivate(self, request, **kwargs):
    #     customer = self.get_object()
    #     customer.active = False
    #     customer.save()
    #
    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)
    #
    # # การใช้ action แบบนี้เป็นการเพิ่ม urlให้มัน ตอนเรียกเราก้อแค่ GET ไปที่ http://localhost:8000/api/customers/3/deactivate/
    # # จะทำให้ active กลายเป็น False ไปเลย คือ เป็ฯการ GET ที่เปลี่ยนค่าได้ หรือเรียกว่า custom actions
    #
    # @action(detail=False)
    # def deactivate_all(self, request,
    #                    **kwargs):  # http://localhost:8000/api/customers/deactivate_all/ แค่นี้ก้อเป็น False หมดเลยทันที ไวมาก
    #     customers = self.get_queryset()
    #     customers.update(active=False)
    #
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=False)
    # def activate_all(self, request,
    #                  **kwargs):  # http://localhost:8000/api/customers/activate_all/ แค่ GET แบบนี้ก้อเป็น True หมดเลยทันที
    #     customers = self.get_queryset()
    #     customers.update(active=True)
    #
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=False, methods=['POST'])  # อันนี้ใช้ method POST  gเพื่อทำการเปลี่ยน status ของ active
    # def change_status(self, request, **kwargs):  # http://localhost:8000/api/customers/change_status/ แต่ต้องใช้ POST method นะ
    #     status = True if request.data['active'] == 'True' else False
    #
    #     customers = self.get_queryset()
    #     customers.update(active=status)
    #
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):  # แบบนี้เราก้อทำได้หมดแล้วนะ ทั้ง GET, POST, PUT, PATCH
    # queryset = Profession.objects.filter(
    #     id=4)  # ถ้าแบบนี้ก้อจะช่วย filter จาก id ที่ 2 ได้เลยเวลาเรียก api 'professions'
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = [
        TokenAuthentication, ]  # บรรทัดนี้ใช้เพื่อทำให้ api viewset อันนี้ต้องใช้ token เข้ามานะ ไม่สามารถ get ได้แบบปกติแล้ว
    permission_classes = [IsAdminUser, ]  # อันนี้จะทำให้้ต้องเป็น admin ที่เป็น staff เท่านั้นจึงจะ GET ได้, ถ้ามีแค่ token อย่างเดียวยังไม่ได้นะ


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]  # ถ้าทำแบบนี้จะทำให้ไม่ต้อง authen ก้อสามารถ get ค่าออกมาได้เลยนะ


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]  #  สามารถ GET ได้แม้ว่าจะไม่่ได้แนบ token เข้ามา, แต่ถ้าจะ POST ต้องแนบ token ใน Headers และใส่ Body เข้ามาด้วย, DELETE ก้อทำได้เช่นกันนะ แค่ใส่ id กับ token เข้าไป



# สรุปนะ ถ้ายังไม่ได้ implement token เข้ามา จะต้องใช้ username+password ทุกครั้ง ไม่งั้นจะฟ้องว่า "detail": "Authentication credentials were not provided."
# แต่ถ้า implement token เข้ามาแล้ว ก้อใช้ username + password ไม่ได้แล้วเช่นกัน ต้องใช้ token แนบเข้ามาใน Header เท่านั้นเพื่อ get ค่าออกมา
# แต่ถ้าต้องการให้ api นั้นไม่มี authen เลยอันเดียวเท่านั้น ก้อให้ไป set allowany แบบนี้ permission_classes = [AllowAny, ]
