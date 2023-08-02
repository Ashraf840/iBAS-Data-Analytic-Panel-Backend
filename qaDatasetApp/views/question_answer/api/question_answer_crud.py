from django.http import HttpResponse
from rest_framework.response import Response
from qaDatasetApp.models import (
    question_answer as qam,
    language as lm)
from django.contrib.auth.models import User
from qaDatasetApp.serializers.question_answer import question_answer as qas
from rest_framework import generics
from qaDatasetApp.mixins import multipleLookupFields as mlf
from rest_framework import status


def test_list(request):
    return HttpResponse('question-answer: test_list')


class AnswerDetail(mlf.MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    # [Resource]
    #   - [General] https://www.agiliq.com/blog/2019/05/django-rest-framework-retrieveupdatedestroyapiview/#retrieveupdatedestroyapiview
    queryset = qam.Answer.objects.all()
    serializer_class = qas.Answer
    lookup_fields = ('pk', 'language', 'created_by')

    def update(self, request, *args, **kwargs):
        # [Update API Solution]
        #   - https://stackoverflow.com/a/31175629
        #   - [Resource - "super().update()"]: https://stackoverflow.com/a/30514296
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)     # calling the 'update' method of "Answer" serializer-class
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)