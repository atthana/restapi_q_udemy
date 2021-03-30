from rest_framework import serializers

from .models import Customer, Profession, Document, DataSheet


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
    datasheet = DataSheetSerializer()
    profession = ProfessionSerializer(
        many=True)  # ใช้ many=True ร่วมด้วย ไม่งั้นมันจะไม่โชว์ค่าจิงๆ แต่จะเป็น core.xxx.xxx แทน
    document_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'profession',
                  'datasheet', 'active', 'status_message',
                  'num_professions', 'document_set'
                  )

    def get_num_professions(self, obj):
        # import pdb; pdb.set_trace()
        return obj.num_professions()

    def get_datasheet(self, obj):
        return obj.datasheet.description


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer',)
