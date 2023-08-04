# from django.http import HttpResponse
from rest_framework.response import Response
from qaDatasetApp.models import question_answer as qam
from qaDatasetApp.serializers.question_answer.question import question as qas
from rest_framework import generics
from qaDatasetApp.mixins import multipleLookupFields as mlf
from rest_framework import status
from qaDatasetApp.mixins.paginator.PageNumberPagination import main


class QuestionList(generics.ListCreateAPIView):
    queryset = qam.Question.objects.all()
    serializer_class = qas.Question
    pagination_class = main.StandardResultsSetPaginationMixin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)     # calling the 'create' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_201_CREATED)
