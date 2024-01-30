from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FinalDataset
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import os
import requests
from rest_framework.response import Response
from rest_framework import status
from .serializers import FinalDatasetSerializer
from rest_framework.decorators import api_view
from qaDatasetApp.models import qa_dataset as qadm
from django.db import connection

@api_view(['GET'])
def get_final_dataset_data(request):
    offset = int(request.query_params.get('offset', 0))/3
    limit = int(request.query_params.get('limit', 0))
    text = request.query_params.get('searchText', '')

    cursor = connection.cursor()

    query = """
    SELECT * FROM public.final_dataset_operations_finaldataset
    WHERE
        bangla_ques ILIKE %s OR
        english_ques ILIKE %s OR
        transliterated_ques ILIKE %s OR
        bangla_ans ILIKE %s OR
        english_ans ILIKE %s
    """

    queryForNoText = """
    SELECT * FROM public.final_dataset_operations_finaldataset
    """

    count = 0   
    if text and not limit:
        cursor.execute(query, ['%' + text + '%'] * 5)
        rows = cursor.fetchall()

        simplified_data = []
        for row in rows:
            count += 1
            bangla_entry = {
                'id': count,
                'did': row[0],
                'question': row[1],
                'answer': row[4],
                'language': 'Bangla',
            }
            simplified_data.append(bangla_entry)

            english_entry = {
                'id': count,
                'did': row[0],
                'question': row[2],
                'answer': row[5],
                'language': 'English',
            }
            simplified_data.append(english_entry)

            transliterated_entry = {
                'id': count,
                'did': row[0],
                'question': row[3],
                'answer': row[4],
                'language': 'Transliterated',
            }
            simplified_data.append(transliterated_entry)
            count = len(rows)

    elif limit and not text:
            limit = limit / 3
            print("limit: ",limit)
            cursor.execute(queryForNoText)
            countRows = cursor.fetchall()
            count = len(countRows)
            cursor.execute(queryForNoText + " OFFSET %s LIMIT %s", [offset, limit])
            rows = cursor.fetchall()
            datCount = 0
            simplified_data = []
            for row in rows:
                datCount += 1
                bangla_entry = {
                    'id': datCount,
                    'did': row[0],
                    'question': row[1],
                    'answer': row[4],
                    'language': 'Bangla',
                }
                simplified_data.append(bangla_entry)

                english_entry = {
                    'id': datCount,
                    'did': row[0],
                    'question': row[2],
                    'answer': row[5],
                    'language': 'English',
                }
                simplified_data.append(english_entry)

                transliterated_entry = {
                    'id': datCount,
                    'did': row[0],
                    'question': row[3],
                    'answer': row[4],
                    'language': 'Transliterated',
                }
                simplified_data.append(transliterated_entry)
    elif limit and text:
            limit = limit / 3
            print("limit: ",limit)
            cursor.execute(query, ['%' + text + '%'] * 5)
            rowCount = cursor.fetchall()
            count = len(rowCount)
            cursor.execute(query + " OFFSET %s LIMIT %s", ['%' + text + '%'] * 5 + [offset, limit])
            rows = cursor.fetchall()
            simplified_data = []
            dataCount = 0

            for row in rows:
                dataCount += 1
                bangla_entry = {
                    'id': dataCount,
                    'did': row[0],
                    'question': row[1],
                    'answer': row[4],
                    'language': 'Bangla',
                }
                simplified_data.append(bangla_entry)

                english_entry = {
                    'id': dataCount,
                    'did': row[0],
                    'question': row[2],
                    'answer': row[5],
                    'language': 'English',
                }
                simplified_data.append(english_entry)

                transliterated_entry = {
                    'id': dataCount,
                    'did': row[0],
                    'question': row[3],
                    'answer': row[4],
                    'language': 'Transliterated',
                }
                simplified_data.append(transliterated_entry)
    else:
        count = 0
        simplified_data = []

    data = {
        'count': count * 3,
        'results': simplified_data
    }

    return Response(data, status=status.HTTP_200_OK)

@csrf_exempt
def add_to_dataset(request):
    if request.method == 'POST':
        record_id = json.loads(request.body)
        record = qadm.QADataset.objects.get(pk=record_id)

        bangla_ques = record.bangla_ques
        english_ques = record.english_ques
        transliterated_ques = record.transliterated_ques
        bangla_ans = record.bangla_ans
        english_ans = record.english_ans
        
        FinalDataset.objects.create(bangla_ques=bangla_ques,transliterated_ques= transliterated_ques, bangla_ans=bangla_ans, english_ques=english_ques, english_ans=english_ans)

        record.flags = True
        record.save()

        return JsonResponse({'message': 'Data added to the dataset'}, status=201)

def clean_database_table(request):
    if request.method == 'GET':
        try:
            FinalDataset.objects.all().delete()
            return JsonResponse({'message': 'Table cleaned successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def start_training(request):
    if request.method == 'GET':
        try:
            create_dataset(request)
            response = requests.get('http://127.0.0.1:5010/train_automation')
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"Start training failed: {str(e)}")
            response_data = {'error': 'Training start failed'}
            return JsonResponse(response_data, status=500)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)


def create_dataset(request):
    if request.method == 'GET':
        data_folder = '/mnt/New Volume/workstation2/source'
        dataset_file = os.path.join(data_folder, 'final_dataset_5column.xlsx')

        data = FinalDataset.objects.all().values( 'bangla_ans', 'bangla_ques', 'english_ans', 'english_ques', 'transliterated_ques')

        try:
            df = pd.read_excel(dataset_file, sheet_name='Sheet1')
            
            df.drop(df.index, inplace=True)
            df.to_excel(dataset_file, index=False)

        except FileNotFoundError:
            df = pd.DataFrame(columns=['bangla_ques', 'transliterated_ques', 'bangla_ans', 'english_ques','english_ans'])

        new_data = pd.DataFrame(data)
        new_data.columns = ['bangla_ques', 'transliterated_ques', 'bangla_ans', 'english_ques','english_ans']

        df = pd.concat([df, new_data], ignore_index=True)

        df.to_excel(dataset_file, sheet_name='Sheet1', index=False)
        print("dataset generated")
        response_data = {'generated': 'data generated'}

        return JsonResponse(response_data)