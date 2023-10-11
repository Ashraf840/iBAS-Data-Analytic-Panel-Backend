# # from django.http import HttpResponse
# from rest_framework.response import Response
# from qaDatasetApp.models import question_answer as qam
# from qaDatasetApp.serializers.question_answer.answer import answer as qas
# from rest_framework import generics
# from qaDatasetApp.mixins import multipleLookupFields as mlf
# from rest_framework import status
# from qaDatasetApp.mixins.paginator.PageNumberPagination import main


# class AnswerDetail(mlf.MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
#     queryset = qam.Answer.objects.all()
#     serializer_class = qas.Answer
#     lookup_fields = ('pk',)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# class AnswerList(generics.ListCreateAPIView):
#     queryset = qam.Answer.objects.all()
#     serializer_class = qas.Answer
#     pagination_class = main.StandardResultsSetPaginationMixin

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
