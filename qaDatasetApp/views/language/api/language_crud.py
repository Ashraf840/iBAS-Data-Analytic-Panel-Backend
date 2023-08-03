from django.http import HttpResponse
from qaDatasetApp.models import language as lm
from qaDatasetApp.serializers.language import language as ls
from rest_framework import generics
from qaDatasetApp.mixins import multipleLookupFields as mlf
from qaDatasetApp.mixins.paginator.PageNumberPagination import main


def test_list(request):
    return HttpResponse('language: test_list')


class LanguageDetail(mlf.MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = lm.Language.objects.all()
    serializer_class = ls.Language
    lookup_fields = ('pk', 'language_name')


class LanguageList(generics.ListCreateAPIView):
    queryset = lm.Language.objects.all()
    serializer_class = ls.Language
    pagination_class = main.StandardResultsSetPaginationMixin
