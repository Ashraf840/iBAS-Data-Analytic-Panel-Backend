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




@api_view(['GET'])
def get_final_dataset_data(request):
    final_dataset_data = FinalDataset.objects.all()
    serializer = FinalDatasetSerializer(final_dataset_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


    # response_data = {"idx": {}}
    # for idx, entry in enumerate(final_dataset_data, start=1):
    #     response_data["idx"][idx] = {
    #         'question': entry.question,
    #         'answer': entry.answer,
    #         'language': entry.language,
    #     }
    # return JsonResponse(response_data)


@csrf_exempt
def add_to_dataset(request):
    if request.method == 'POST':
        record_id = json.loads(request.body)
        record = qadm.QADataset.objects.get(pk=record_id)
        # print(record_id)
        bangla_ques = record.bangla_ques
        english_ques = record.english_ques
        transliterated_ques = record.transliterated_ques
        bangla_ans = record.bangla_ans
        english_ans = record.english_ans
        # print(bangla_ques, english_ques, transliterated_ques, bangla_ans, english_ans)

        if bangla_ques and bangla_ans:
            FinalDataset.objects.create(question=bangla_ques, answer=bangla_ans, language='Bangla')
        if english_ques and english_ans:
            FinalDataset.objects.create(question=english_ques, answer=english_ans, language='English')

        if transliterated_ques and bangla_ans:
            FinalDataset.objects.create(question=transliterated_ques, answer=bangla_ans, language='Transliterated')
        
        record.flags = True
        record.save()

        return JsonResponse({'message': 'Data added to the dataset'}, status=201)









        #####################################################################################3
        data = json.loads(request.body)
        bangla_ques = data.get('bangla_ques')
        english_ques = data.get('english_ques')
        transliterated_ques = data.get('transliterated_ques')
        bangla_ans = data.get('bangla_ans')
        english_ans = data.get('english_ans')

        # Create entries in the FinalDataset model based on the provided data
        if bangla_ques and bangla_ans:
            FinalDataset.objects.create(question=bangla_ques, answer=bangla_ans, language='Bangla')
        if english_ques and english_ans:
            FinalDataset.objects.create(question=english_ques, answer=english_ans, language='English')

        if transliterated_ques and bangla_ans:
            FinalDataset.objects.create(question=transliterated_ques, answer=bangla_ans, language='Transliterated')

        return JsonResponse({'message': 'Data added to the dataset'}, status=201)
        #####################################################################################3
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



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
            response_data = {'message': 'Training started'}
            return JsonResponse(response_data, status=200)

            response = requests.get('http://127.0.0.1:5000/train_automation')
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
        data_folder = '/home/tanjim/workstation/ibas-chat-operator/data/'
        dataset_file = os.path.join(data_folder, 'ibas_final_dataset.xlsx')

        # Retrieve data from the database
        data = FinalDataset.objects.all().values('index', 'question', 'answer', 'language')

        # Create or load the dataset
        try:
            df = pd.read_excel(dataset_file, sheet_name='Sheet1')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Index', 'Questions', 'Answers', 'Language'])

        # Create a new DataFrame with the database data
        new_data = pd.DataFrame(data)
        new_data.columns = ['Index', 'Questions', 'Answers', 'Language']

        # Concatenate the new data with the existing dataset
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the dataset to the Excel file
        df.to_excel(dataset_file, sheet_name='Sheet1', index=False)
        print("dataset generated")
        response_data = {'generated': 'data generated'}

        return JsonResponse(response_data)