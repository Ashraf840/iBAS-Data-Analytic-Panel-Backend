from rest_framework import serializers
from .models import FinalDataset


class FinalDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalDataset
        fields = '__all__'