# from rest_framework import serializers
# from qaDatasetApp.models import (
#     question_answer as qam,
#     language as lm)
# from ...language import language as ls
# from django.contrib.auth.models import User


# class Answer(serializers.ModelSerializer):
#     language = serializers.SlugRelatedField(
#         queryset=lm.Language.objects.all(),
#         slug_field='language_name'
#     )
#     #  Depict username instead of user-id.
#     created_by = serializers.SlugRelatedField(
#         queryset=User.objects.all(),
#         slug_field='username'
#     )

#     class Meta:
#         model = qam.Answer
#         fields = '__all__'

#     def create(self, validated_data):
#         # language_val = dict(validated_data.pop('language', ''))
#         # language = lm.Language.get_object(**dict(validated_data.pop('language', '')))

#         # After fetching the "Langauge" object, inject that while creating an "Answer" object.
#         return qam.Answer.objects.create(
#             answer=validated_data.get('answer'),
#             # language=language,
#             language=validated_data.get('language'),
#             created_by=validated_data.get('created_by')
#         )

#     def update(self, instance, validated_data):
#         instance.answer, instance.language, instance.created_by = \
#             validated_data.get('answer'), validated_data.get('language'), validated_data.get('created_by')
#         instance.save()
#         return instance
