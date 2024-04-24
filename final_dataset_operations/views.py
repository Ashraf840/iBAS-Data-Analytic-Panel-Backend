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


@api_view(['POST'])
def get_final_dataset_data(request):
    offset = int(request.query_params.get('offset', 0))/3
    limit = int(request.query_params.get('limit', 0))/3
    text = request.query_params.get('searchText', '')

    if request.body:
        try:
            data = json.loads(request.body)
            training_status = data.get('status', None)
            print("BODY: ", training_status)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        training_status = None

    cursor = connection.cursor()

    query = f"""
    SELECT * FROM public.final_dataset_operations_finaldataset
    WHERE 1 = 1
    ORDER BY id DESC
    """

    if training_status:
        query += f" AND status = '{training_status}'"
    
    if text:
        query += f""" AND ( bangla_ques ILIKE '%{text}%' OR
          english_ques ILIKE '%{text}%' OR
          transliterated_ques ILIKE '%{text}%' OR
          bangla_ans ILIKE '%{text}%' OR
          english_ans ILIKE '%{text}%') """
    
    cursor.execute(query)
    countRows = cursor.fetchall()
    totalcount = len(countRows)
        
    if limit:
        query += f" limit {limit}"

    if offset:
        query += f" offset {offset}"

    cursor.execute(query)
    rows = cursor.fetchall()
    count = 0 
    simplified_data = []
    for row in rows:
        count += 1
        bangla_entry = {
            'id': count,
            'oid': row[0],
            'question': row[1],
            'answer': row[4],
            'language': 'Bangla',
            'status' : row[6],
        }
        simplified_data.append(bangla_entry)

        english_entry = {
            'id': count,
            'oid': row[0],
            'question': row[2],
            'answer': row[5],
            'language': 'English',
            'status' : row[6],
        }
        simplified_data.append(english_entry)

        transliterated_entry = {
            'id': count,
            'oid': row[0],
            'question': row[3],
            'answer': row[4],
            'language': 'Transliterated',
            'status' : row[6],

        }
        simplified_data.append(transliterated_entry)
    
    data = {
        'count': totalcount * 3,
        'results': simplified_data
    }

    return Response(data, status=status.HTTP_200_OK)


# # ORIGINAL ****************************
# @api_view(['POST'])
# def get_final_dataset_data(request):
#     offset = int(request.query_params.get('offset', 0))/3
#     limit = int(request.query_params.get('limit', 0))/3
#     text = request.query_params.get('searchText', '')
#     data = json.loads(request.body)
#     training_status = data.get('status', None)
#     print("BODY: ", training_status)

#     cursor = connection.cursor()

#     query = f"""
#     SELECT * FROM public.final_dataset_operations_finaldataset
#     WHERE 1 = 1
#     """

#     if training_status:
#         query += f" AND status = '{training_status}'"
    
#     if text:
#         query += f""" AND ( bangla_ques ILIKE '%{text}%' OR
#           english_ques ILIKE '%{text}%' OR
#           transliterated_ques ILIKE '%{text}%' OR
#           bangla_ans ILIKE '%{text}%' OR
#           english_ans ILIKE '%{text}%') """
    
#     cursor.execute(query)
#     countRows = cursor.fetchall()
#     totalcount = len(countRows)
        
#     if limit:
#         query += f" limit {limit}"

#     if offset:
#         query += f" offset {offset}"

#     cursor.execute(query)
#     rows = cursor.fetchall()
#     count = 0 
#     simplified_data = []
#     for row in rows:
#         count += 1
#         bangla_entry = {
#             'id': count,
#             'oid': row[0],
#             'question': row[1],
#             'answer': row[4],
#             'language': 'Bangla',
#             'status' : row[6],
#         }
#         simplified_data.append(bangla_entry)

#         english_entry = {
#             'id': count,
#             'oid': row[0],
#             'question': row[2],
#             'answer': row[5],
#             'language': 'English',
#             'status' : row[6],
#         }
#         simplified_data.append(english_entry)

#         transliterated_entry = {
#             'id': count,
#             'oid': row[0],
#             'question': row[3],
#             'answer': row[4],
#             'language': 'Transliterated',
#             'status' : row[6],

#         }
#         simplified_data.append(transliterated_entry)
    
#     data = {
#         'count': totalcount * 3,
#         'results': simplified_data
#     }

#     return Response(data, status=status.HTTP_200_OK)

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
            # create_dataset(request)   # Make a backup of nul.yml, domain.yml, rules.yml, stories.yml file
            response = requests.get('http://127.0.0.1:5010/train_automation')
            print("Start training automation response:", json.loads(response.text))
            # response.raise_for_status()
            response_data = json.loads(response.text)
            return JsonResponse(response_data, status=200)
            
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