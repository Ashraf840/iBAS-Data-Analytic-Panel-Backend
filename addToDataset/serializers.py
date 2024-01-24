from rest_framework import serializers
from .models import SuggestiveQuestions


class SuggestiveQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestiveQuestions
        fields = '__all__'
