# from django.http import HttpResponse
from rest_framework.response import Response
from qaDatasetApp.models import question_answer as qam
from qaDatasetApp.serializers.question_answer.question import question as qas
from rest_framework import generics
from qaDatasetApp.mixins import multipleLookupFields as mlf
from rest_framework import status
from qaDatasetApp.mixins.paginator.PageNumberPagination import main


class QuestionDetail(mlf.MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = qam.Question.objects.all()
    serializer_class = qas.Question
    # lookup_fields = ('pk', 'answer', 'language', 'created_by')  # TURNED OFF, SINCE THROWING "MultipleObjectReturned" error.
    lookup_fields = ('pk',)     # NOT NECESSARY TO USE THIS LOC, OR THE 'MultipleFieldLookupMixin', SINCE OTHER FOREIGNKEYFIELD LOOKUP WILL THROW ERROR WHEN FINDS MULTIPLE RECORD.

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)     # calling the 'update' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class QuestionList(generics.ListCreateAPIView):
    queryset = qam.Question.objects.all()
    serializer_class = qas.Question
    pagination_class = main.StandardResultsSetPaginationMixin   # 20 records/page; max-total-page: 1000

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)     # calling the 'create' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_201_CREATED)
