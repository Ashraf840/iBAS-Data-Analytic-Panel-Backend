from rest_framework import serializers
from qaDatasetApp.models import (
    question_answer as qam,
    language as lm)
from ...language import language as ls
from django.contrib.auth.models import User


class Answer(serializers.ModelSerializer):
    # [Resource]
    #   - [Update Nested Serializer]
    #       https://django.cowhite.com/blog/create-and-update-django-rest-framework-nested-serializers/
    # language = ls.Language()  # NOT USING, SINCE this LOC is throwing error while using API platform for creating new Answer record.
    # Changed since issue raised while creating new Answer through Insomnia / Postman.
    # Furthermore, change the fetching method of "language" in the create() method of this serializer-class.
    language = serializers.SlugRelatedField(
        queryset=lm.Language.objects.all(),
        slug_field='language_name'
    )
    #  Depict username instead of user-id.
    # [Solution - Depict Username instead of user id]
    #   - https://www.sankalpjonna.com/learn-django/representing-foreign-key-values-in-django-serializers
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = qam.Answer
        fields = '__all__'

    def create(self, validated_data):
        # [Resource - "Writable Nested Serializer"]: https://stackoverflow.com/a/34785475
        # pop-out the "language-ordered-dict", from which the language-object will be fetched from the "Langauge" model.
        # language_val = dict(validated_data.pop('language', ''))   # [NOT NECESSARY, INJECTED STRAIGHT BELOW]
        # language = lm.Language.get_object(**dict(validated_data.pop('language', '')))   # NOT USING, SINCE API-PLATFORMS THROWING ERROR

        # After fetching the "Langauge" object, inject that while creating an "Answer" object.
        # TODO: Add a try-catch block below whereas in the catch-block, return an error-message as dictionary,
        #  since it'll be return to Response(passedData) of the "AnswerList" class. Thus, there will be
        #  2 separate returns in those try-catch-block.
        return qam.Answer.objects.create(
            answer=validated_data.get('answer'),
            # language=language,
            language=validated_data.get('language'),
            created_by=validated_data.get('created_by')
        )

    def update(self, instance, validated_data):
        # [Update API Solution]
        #   - https://stackoverflow.com/a/73632174
        #   - https://stackoverflow.com/a/33077927
        #   - https://stackoverflow.com/a/65972405
        # language_val, user_val = dict(validated_data.pop('language', '')), validated_data.pop('created_by', '')   # NOT USING THIS APPROACH; SINCE THROWING ERROR WHILE UISNG API-PLATFORMS INSTEAD OF DRF-WEB-UI
        # instance = super().update(instance, validated_data)
        # language = lm.Language.get_object(**language_val)
        # instance.language, instance.created_by = language, user_val

        instance.answer, instance.language, instance.created_by = \
            validated_data.get('answer'), validated_data.get('language'), validated_data.get('created_by')
        instance.save()
        return instance