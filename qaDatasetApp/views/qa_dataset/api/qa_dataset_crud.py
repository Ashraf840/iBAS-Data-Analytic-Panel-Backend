from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from qaDatasetApp.models import qa_dataset as qadm
from qaDatasetApp.serializers.qa_dataset import qa_dataset as qads
from qaDatasetApp.mixins.paginator.PageNumberPagination import main
from qaDatasetApp.mixins import multipleLookupFields as mlf


class QADatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = qadm.QADataset.objects.all()
    serializer_class = qads.QADataset
    lookup_fields = ('pk',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print("sth")
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class QADatasetList(generics.ListCreateAPIView):
    queryset = qadm.QADataset.objects.filter(flags=False).order_by('id')
    serializer_class = qads.QADataset
    pagination_class = main.StandardResultsSetPaginationMixin

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 0))
        text = request.query_params.get('searchText')

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        if text:
            queryset = queryset.filter(
            bangla_ques__icontains=text,
            english_ques__icontains=text,
            transliterated_ques__icontains=text,
            bangla_ans__icontains=text,
            english_ans__icontains=text
            )
            print ("text")

            count = queryset.count()

        elif limit:
            queryset = queryset[offset: offset + limit]
            print("limit")
        elif limit and text:
            queryset = queryset.filter(
                bangla_ques__icontains==text |
                english_ques__icontains==text |
                transliterated_ques__icontains==text |
                bangla_ans__icontains==text |
                english_ans__icontains==text
            )[offset:offset + limit]
            print("limit and text")
            
        
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'count': count,
            'results': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
# class YourModelListView(ListAPIView):
#     serializer_class = YourModelSerializer
#     queryset = YourModel.objects.all()

#     def list(self, request, *args, **kwargs):
#         offset = int(request.query_params.get('offset', 0))
#         limit = int(request.query_params.get('limit', 0))
#         text = request.query_params.get('searchText', '')

#         queryset = self.filter_queryset(self.get_queryset())

#         if text:
#             # Search the text in all relevant fields
#             queryset = queryset.filter(
#                 bangla_ques__icontains==text |
#                 english_ques__icontains==text |
#                 transliterated_ques__icontains==text |
#                 bangla_ans__icontains==text |
#                 english_ans__icontains==text
#             )

#         count = queryset.count()

#         if limit:
#             # Apply pagination
#             queryset = queryset[offset: offset + limit]

#         serializer = self.get_serializer(queryset, many=True)

#         data = {
#             'count': count,
#             'results': serializer.data
#         }

#         return Response(data, status=status.HTTP_200_OK)

# class QADatasetList(generics.ListCreateAPIView):
#     queryset = qadm.QADataset.objects.filter(flags=False).order_by('id')
#     serializer_class = qads.QADataset
#     pagination_class = main.StandardResultsSetPaginationMixin
#     print("here")

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         print("here")
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
