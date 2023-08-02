from rest_framework import serializers
from qaDatasetApp.models import language


class Language(serializers.ModelSerializer):
    class Meta:
        model = language.Language
        fields = '__all__'
