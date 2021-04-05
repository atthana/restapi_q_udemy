from rest_framework import serializers

from .models import Customer, Profession, Document, DataSheet


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer',)


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data',)


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description', 'status')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    datasheet = DataSheetSerializer(read_only=True)
    profession = ProfessionSerializer(
        many=True)  # ใช้ many=True ร่วมด้วย ไม่งั้นมันจะไม่โชว์ค่าจิงๆ แต่จะเป็น core.xxx.xxx แทน
    document_set = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'profession',
                  'datasheet', 'active', 'status_message',
                  'num_professions', 'document_set'
                  )

    def create(self, validated_data):

        # จริงๆจะทำแบบไหนก้อได้นะคือ ดึงออกมาแล้วค่อย del หรือ จะ pop ออกมาเลยก็ได้
        professions = validated_data['profession']  # เอามาเก็บในตัวแปรก่อน

        del validated_data['profession']  # เสดแล้วก้อลบทิ้งไป

        customer = Customer.objects.create(**validated_data)  # จากนั้นค่อย create ส่วน customer ข้างในที่ไม่มี nested

        for profession in professions:  # แล้วก็มาทำส่วน profession ที่เป็น nested โดยใช้ for loop
            prof = Profession.objects.create(**profession)  # create ในส่วนของ Profession
            customer.profession.add(prof)  # เมือ create แล้วจะได้ prof ก็เอามา add เข้าไปใน customer.profession ตามเดิม

        customer.save()  # เสดแล้วค่อยมา save และ return ออกไป

        return customer

        # if validated_data['profession'] is not None:  #  ต้องถามกู๊กกิ๊กว่าทำไม เราทำแบบที่โบนัสสอน แต่มันได้ post ทีละ 2อันเลย
        #     professions = validated_data.pop('profession', None)
        #
        # customer = Customer.objects.create(**validated_data)
        # for profession in professions:
        #     prof = Profession.objects.create(**profession)
        #     customer.profession.add(prof)
        #
        # customer.save()
        # return customer
        # return super(CustomerSerializer, self).create(validated_data=validated_data)

    def get_num_professions(self, obj):
        # import pdb; pdb.set_trace()
        return obj.num_professions()

    def get_datasheet(self, obj):
        return obj.datasheet.description
