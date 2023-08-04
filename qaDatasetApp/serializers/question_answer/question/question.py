from rest_framework import serializers
from qaDatasetApp.models import (
    question_answer as qam,
    language as lm)
# from ...language import language as ls
from django.contrib.auth.models import User
# from ..answer.answer import Answer


class Question(serializers.ModelSerializer):
    # answer = Answer()
    # language = ls.Language()
    answer = serializers.SlugRelatedField(
        queryset=qam.Answer.objects.all(),
        slug_field='answer'
    )
    language = serializers.SlugRelatedField(
        queryset=lm.Language.objects.all(),
        slug_field='language_name'
    )
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = qam.Question
        fields = '__all__'

    def create(self, validated_data):
        # pop-out "language-object" and get the language-name-field only as a dict
        # language_val = validated_data.get('language')
        # lang_dict = dict()
        # lang_dict['language_name'] = language_val.language_name
        # lang_dict = {'language_name': language_val.language_name}
        # language = lm.Language.get_object(**{'language_name': language_val.language_name})
        # MORE PRECISE
        # language = lm.Language.get_object(**{'language_name': validated_data.get('language').language_name})

        # TODO: Add a try-catch block below whereas in the catch-block, return an error-message as dictionary,
        #  since it'll be return to Response(passedData) of the "AnswerList" class. Thus, there will be
        #  2 separate returns in those try-catch-block.
        return qam.Question.objects.create(
            question=validated_data.get('question'),
            answer=validated_data.get('answer'),
            language=validated_data.get('language'),
            created_by=validated_data.get('created_by')
        )

    def update(self, instance, validated_data):
        instance.question, instance.answer, instance.language, instance.created_by = \
            validated_data.get('question'), validated_data.get('answer'), validated_data.get('language'), validated_data.get('created_by')
        instance.save()
        return instance
