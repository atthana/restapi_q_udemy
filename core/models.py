from django.db import models


class Profession(models.Model):
    description = models.CharField(max_length=50)


class DataSheet(models.Model):
    description = models.CharField(max_length=50)
    historical_data = models.TextField()

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    profession = models.ManyToManyField(Profession)
    datasheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    @property
    def status_message(self):  # เราสามารถสร้าง property field ขึ้นมาเปรียบเสมือน มีอีก field นึงให้ serializer พ่นออกไปได้เลย
        #  อย่างในเคสนี้ก้อให้มัน follow กับ active ข้างบน และโชว์ออกไปเป็น wording ที่เราต้องการ แต่ต้องเพิ่ม field ใน serializer ด้วยนะ
        if self.active:
            return 'Customer active'
        else:
            return 'Customer not active'

    def __str__(self):
        return self.name


class Document(models.Model):
    PP = 'PP'
    ID = 'ID'
    OT = 'OT'

    DOC_TYPES = (
        (PP, 'Passport'),
        (ID, 'Identity card'),
        (OT, 'Others')
    )

    dtype = models.CharField(choices=DOC_TYPES, max_length=2)
    doc_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
