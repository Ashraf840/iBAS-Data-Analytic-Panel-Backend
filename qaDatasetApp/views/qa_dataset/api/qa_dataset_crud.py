# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from qaDatasetApp.models import qa_dataset as qadm
from qaDatasetApp.serializers.qa_dataset import qa_dataset as qads
from qaDatasetApp.mixins.paginator.PageNumberPagination import main
from qaDatasetApp.mixins import multipleLookupFields as mlf


def test_list(request):
    return HttpResponse('qa-dataset: test_list')


class QADatasetDetail(mlf.MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = qadm.QADataset.objects.all()
    serializer_class = qads.QADataset
    lookup_fields = ('pk',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)     # calling the 'update' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class QADatasetList(generics.ListCreateAPIView):
    queryset = qadm.QADataset.objects.all()
    serializer_class = qads.QADataset
    pagination_class = main.StandardResultsSetPaginationMixin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)     # calling the 'create' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_201_CREATED)
