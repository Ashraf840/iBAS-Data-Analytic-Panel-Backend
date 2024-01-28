from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from qaDatasetApp.models import qa_dataset as qadm
from qaDatasetApp.serializers.qa_dataset import qa_dataset as qads
from qaDatasetApp.mixins.paginator.PageNumberPagination import main
from qaDatasetApp.mixins import multipleLookupFields as mlf
from django.db.models import Q
from django.db import connection

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
        cursor = connection.cursor()

        query = """
        SELECT * FROM public."qaDatasetApp_qadataset"
        WHERE
            bangla_ques ILIKE %s OR
            english_ques ILIKE %s OR
            transliterated_ques ILIKE %s OR
            bangla_ans ILIKE %s OR
            english_ans ILIKE %s
        """


        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        if text and not limit:
            cursor.execute(query, ['%' + text + '%'] * 5)
            rows = cursor.fetchall()
            count = len(rows)
            queryset = []
            for row in rows:
                print("***********ROW:", row)
                result = {
                    'id': row[0],
                    'bangla_ques': row[1],
                    'english_ques': row[2],
                    'transliterated_ques': row[3],
                    'bangla_ans': row[4],
                    'english_ans': row[5],
                    'created_at': row[6],
                    'update_at': row[7],
                    'flags': row[8]
                }
                queryset.append(result)

        elif limit and not text:
            queryset = queryset[offset: offset + limit]
            print("limit")
        elif limit and text:
            cursor.execute(query, ['%' + text + '%'] * 5)
            row = cursor.fetchall()
            count = len(row)
            cursor.execute(query + " OFFSET %s LIMIT %s", ['%' + text + '%'] * 5 + [offset, limit])
            rows = cursor.fetchall()

            queryset = []
            for row in rows:
                result = {
                    'id': row[0],
                    'bangla_ques': row[1],
                    'english_ques': row[2],
                    'transliterated_ques': row[3],
                    'bangla_ans': row[4],
                    'english_ans': row[5],
                    'created_at': row[6],
                    'update_at': row[7],
                    'flags': row[8]
                }
                queryset.append(result)
            
        
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'count': count,
            'results': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)