from django.shortcuts import render, HttpResponse
from qaDatasetApp.models import qa_dataset as qadm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import os
from .models import SuggestiveQuestions
from .serializers import SuggestiveQuestionsSerializer


@api_view(['POST'])
def addToDataset(request):
    if request.method == "POST":
        print(request.data)
        record_id = request.data
        return Response({'msg': 'Added to dataset'}, status=status.HTTP_200_OK)
        
        try:
            # Query the database to retrieve the specific record by its ID
            record = qadm.QADataset.objects.get(pk=record_id)
            
            # Extract the fields you want from the record
            bangla_ques = record.bangla_ques
            english_ques = record.english_ques
            tranliterated_ques = record.transliterated_ques
            bangla_ans = record.bangla_ans
            english_ans = record.english_ans

            # You can return these fields in the response
            data = {
                'bangla_ques': bangla_ques,
                'english_ques': english_ques,
                'tranliterated_ques': tranliterated_ques,
                'bangla_ans': bangla_ans,
                'english_ans': english_ans,
            }
            print("data:",data)

            new_update_dataset = '/home/tanjim/workstation/ibas-project/ibas-chat-operator-chatbot/data/ibas_final_dataset.xlsx'
            existing_df = pd.read_excel(new_update_dataset, sheet_name='Sheet1', engine='openpyxl')
            data1 = pd.DataFrame({'Questions': [bangla_ques], 'Answers': [bangla_ans]})
            data2 = pd.DataFrame({'Questions': [tranliterated_ques], 'Answers': [bangla_ans]})
            data3 = pd.DataFrame({'Questions': [english_ques], 'Answers': [english_ans]})

            updated_df = pd.concat([existing_df, data1, data2, data3], ignore_index=True)
            updated_df.to_excel(new_update_dataset, index=False, engine='openpyxl')

            record.flags = True
            record.save()

            return Response(data, status=status.HTTP_200_OK)

        except qadm.QADataset.DoesNotExist:
            return Response({'msg': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'msg': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def pushSuggestiveQA(request):
    if request.method == "GET":
        xlsx_file_path = '/home/zubair/workstation_2/source/paraphrased_texts.xlsx'
        if os.path.exists(xlsx_file_path):
            try:
                df = pd.read_excel(xlsx_file_path, sheet_name='Sheet1')
                for index, row in df.iterrows():
                    text=row['ParaphrasedText']
                    # questions = SuggestiveQuestions.objects.filter(marked_for_removal=False)
                    # serializer = SuggestiveQuestionsSerializer(questions, many=True)
                    entry = SuggestiveQuestions(text=text,)
                    entry.save()
                return Response({'msg': 'Successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return HttpResponse(f'Error importing questions: {str(e)}')
        return Response({'msg': 'Get all suggestive qna'}, status=status.HTTP_200_OK)
    if request.method == "POST":
        pass


# Suggestive QnA
@api_view(['GET', 'POST'])
def suggestiveQA(request):
    if request.method == "GET":
        try:
            questions = SuggestiveQuestions.objects.filter(marked_for_removal=False)
            serializer = SuggestiveQuestionsSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(f'Error importing questions: {str(e)}')
        return Response({'msg': 'Get all suggestive qna'}, status=status.HTTP_200_OK)
    if request.method == "POST":
        pass

@api_view(['GET'])
def genSuggestiveQa(request):
    if request.method == "GET":
        return Response({'msg': 'generate suggestive question QA'}, status=status.HTTP_200_OK)
    return Response({'status': 'succes'}, status=status.HTTP_200_OK)
    pass