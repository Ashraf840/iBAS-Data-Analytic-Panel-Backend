from rest_framework import serializers
from qaDatasetApp.models import (
    question_answer as qam,
    qa_dataset as qadm)
from django.contrib.auth.models import User


class QADataset(serializers.ModelSerializer):
    bangla_ques = serializers.SlugRelatedField(
        queryset=qam.Question.objects.all(),
        slug_field='question'
    )
    english_ques = serializers.SlugRelatedField(
        queryset=qam.Question.objects.all(),
        slug_field='question'
    )
    transliterated_ques = serializers.SlugRelatedField(
        queryset=qam.Question.objects.all(),
        slug_field='question'
    )
    bangla_ans = serializers.SlugRelatedField(
        queryset=qam.Answer.objects.all(),
        slug_field='answer'
    )
    english_ans = serializers.SlugRelatedField(
        queryset=qam.Answer.objects.all(),
        slug_field='answer'
    )
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

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
            created_by=validated_data.get('created_by')
        )

    def update(self, instance, validated_data):
        instance.bangla_ques, instance.english_ques, instance.transliterated_ques, \
            instance.bangla_ans, instance.english_ans, instance.created_by = \
            validated_data.get('bangla_ques'), validated_data.get('english_ques'), \
            validated_data.get('transliterated_ques'), validated_data.get('bangla_ans'), \
            validated_data.get('english_ans'), validated_data.get('created_by')
        instance.save()
        return instance
