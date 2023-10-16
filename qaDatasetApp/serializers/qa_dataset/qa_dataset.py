from rest_framework import serializers
from qaDatasetApp.models import qa_dataset as qadm
from addToDataset.models import SuggestiveQuestions
from django.db.models import Q


class QADataset(serializers.ModelSerializer):
    class Meta:
        model = qadm.QADataset
        fields = '__all__'

    def create(self, validated_data):
        return qadm.QADataset.objects.create(
            bangla_ques=validated_data.get('bangla_ques'),
            english_ques=validated_data.get('english_ques'),
            transliterated_ques=validated_data.get('transliterated_ques'),
            bangla_ans=validated_data.get('bangla_ans'),
            english_ans=validated_data.get('english_ans'),
            # created_by=validated_data.get('created_by')
        )

    def update(self, instance, validated_data):
        instance.bangla_ques, instance.english_ques, instance.transliterated_ques, \
            instance.bangla_ans, instance.english_ans = \
            validated_data.get('bangla_ques'), validated_data.get('english_ques'), \
            validated_data.get('transliterated_ques'), validated_data.get('bangla_ans'), \
            validated_data.get('english_ans')
        instance.save()
        return instance
