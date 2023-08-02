from rest_framework import serializers
from qaDatasetApp.models import (
    question_answer as qam,
    language as lm)
from ..language import language as ls


class Answer(serializers.ModelSerializer):
    # [Resource]
    #   - [Update Nested Serializer] https://django.cowhite.com/blog/create-and-update-django-rest-framework-nested-serializers/
    language = ls.Language()

    class Meta:
        model = qam.Answer
        fields = '__all__'

    def update(self, instance, validated_data):
        # [Update API Solution]
        #   - https://stackoverflow.com/a/73632174
        #   - https://stackoverflow.com/a/33077927
        #   - https://stackoverflow.com/a/65972405
        language_val, user_val = dict(validated_data.pop('language', '')), validated_data.pop('created_by', '')
        instance = super().update(instance, validated_data)
        language = lm.Language.get_object(**language_val)
        instance.language, instance.created_by = language, user_val
        instance.save()
        return instance
