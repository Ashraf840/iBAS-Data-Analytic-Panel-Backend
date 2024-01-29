from django.core.management.base import BaseCommand
import pandas as pd
from openpyxl import load_workbook
from langdetect import detect
from final_dataset_operations.models import FinalDataset

class Command(BaseCommand):
    help = 'Import data from Excel file into FinalDataset model'

    def handle(self, *args, **options):
        excel_file = '/home/doer/Music/ChatBot/ibas-data-analytics-panel-backend/ibas_final_dataset.xlsx'
        # excel_file = '/home/doer/Music/ChatBot/ibas-data-analytics-panel-backend/Final-updated-dataset.xlsx'

        data = pd.read_excel(excel_file, engine='openpyxl')

        for _, row in data.iterrows():
            bangla_ques = row['bangla_ques']
            transliterated_ques = row['transliterated_ques']
            bangla_ans = row['bangla_ans']
            english_ques = row['english_ques']
            english_ans = row['english_ans']

            entry = FinalDataset(
                bangla_ques=bangla_ques,
                transliterated_ques=transliterated_ques,
                bangla_ans=bangla_ans,
                english_ques=english_ques,
                english_ans=english_ans,
            )
            entry.save()
