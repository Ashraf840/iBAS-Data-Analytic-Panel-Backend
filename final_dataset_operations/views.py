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

#### If you want to use serializer use the following block of the code #####

# @api_view(['GET'])
# def get_final_dataset_data(request):
#     final_dataset_data = FinalDataset.objects.all()
#     serializer = FinalDatasetSerializer(final_dataset_data, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

######################################################
@api_view(['GET'])
def get_final_dataset_data(request):
    # final_dataset_data = FinalDataset.objects.all()

    # count = 0
    
    # simplified_data = []
    # for entry in final_dataset_data:
    #     count += 1
    #     # print("id:", count)
    #     bangla_entry = {
    #         'id': count,
    #         'question': entry.bangla_ques,
    #         'answer': entry.bangla_ans,
    #         'language': 'Bangla',
    #     }
    #     print("Bangla entry: ", bangla_entry)
    #     simplified_data.append(bangla_entry)

    #     english_entry = {
    #         'id': count,
    #         'question': entry.english_ques,
    #         'answer': entry.english_ans,
    #         'language': 'English',
    #     }
    #     simplified_data.append(english_entry)

    #     transliterated_entry = {
    #         'id': count,
    #         'question': entry.transliterated_ques,
    #         'answer': entry.bangla_ans, 
    #         'language': 'Transliterated',
    #     }
    #     simplified_data.append(transliterated_entry)
    
    # # Alternatively, you can use list comprehension for a more concise code:
    # # simplified_data = [
    # #     {'question': entry.bangla_ques, 'answer': entry.bangla_ans, 'language': 'Bangla'} for entry in final_dataset_data
    # # ] + [
    # #     {'question': entry.english_ques, 'answer': entry.english_ans, 'language': 'English'} for entry in final_dataset_data
    # # ] + [
    # #     {'question': entry.transliterated_ques, 'answer': entry.bangla_ans, 'language': 'Transliterated'} for entry in final_dataset_data
    # # ]

    # return Response(simplified_data, status=status.HTTP_200_OK)

    offset = int(request.query_params.get('offset', 0))
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
            limit = limit / 5
            print("limit: ",limit)
            queryset = queryset[offset: offset + limit]
    elif limit and text:
            limit = limit / 5
            print("limit: ",limit)
            cursor.execute(query, ['%' + text + '%'] * 5)
            row = cursor.fetchall()
            cursor.execute(query + " OFFSET %s LIMIT %s", ['%' + text + '%'] * 5 + [offset, limit])
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
            count = len(row)
    else:
        count = 0
        simplified_data = []

    data = {
        'count': count,
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
            # Delete all records from the FinalDataset model
            FinalDataset.objects.all().delete()
            return JsonResponse({'message': 'Table cleaned successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def start_training(request):
    if request.method == 'GET':
        try:
            # response_data = {'message': 'Training started'}
            # return JsonResponse(response_data, status=200)
            create_dataset(request)
            # response = requests.get('http://127.0.0.1:5000/train_automation')
            response = requests.get('http://127.0.0.1:5010/train_automation')
            response.raise_for_status()  # Check for HTTP request errors
            
        except requests.exceptions.RequestException as e:
            print(f"Start training failed: {str(e)}")
            response_data = {'error': 'Training start failed'}
            return JsonResponse(response_data, status=500)
    else:
        response_data = {'error': 'Invalid request method'}
        return JsonResponse(response_data, status=400)


# import pandas as pd
def create_dataset(request):
    if request.method == 'GET':
        # data_folder = '/home/tanjim/workstation/ibas-project/source'
        data_folder = '/mnt/New Volume/workstation2/source'
        dataset_file = os.path.join(data_folder, 'final_dataset_5column.xlsx')

        # Retrieve data from the database
        data = FinalDataset.objects.all().values( 'bangla_ans', 'bangla_ques', 'english_ans', 'english_ques', 'transliterated_ques')

        # Create or load the dataset
        try:
            df = pd.read_excel(dataset_file, sheet_name='Sheet1')
            
            df.drop(df.index, inplace=True)
            df.to_excel(dataset_file, index=False)

        except FileNotFoundError:
            df = pd.DataFrame(columns=['bangla_ques', 'transliterated_ques', 'bangla_ans', 'english_ques','english_ans'])

        # Create a new DataFrame with the database data
        new_data = pd.DataFrame(data)
        new_data.columns = ['bangla_ques', 'transliterated_ques', 'bangla_ans', 'english_ques','english_ans']

        # Concatenate the new data with the existing dataset
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the dataset to the Excel file
        df.to_excel(dataset_file, sheet_name='Sheet1', index=False)
        print("dataset generated")
        response_data = {'generated': 'data generated'}

        return JsonResponse(response_data)