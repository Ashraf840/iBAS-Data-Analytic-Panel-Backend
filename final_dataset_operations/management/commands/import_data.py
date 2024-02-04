from django.core.management.base import BaseCommand
import pandas as pd
from openpyxl import load_workbook
from langdetect import detect
from final_dataset_operations.models import FinalDataset

class Command(BaseCommand):
    help = 'Import data from Excel file into FinalDataset model'

    def handle(self, *args, **options):
        excel_file = '/home/ubuntu/ibas_project/source/TADAspreadsheet.xlsx'

        data = pd.read_excel(excel_file, engine='openpyxl')
        FinalDataset.objects.all().delete()
        # Define a function to detect the language
         #def detect_language(text):
          #  try:
           #     return detect(text)
            #except:
             #   return 'Unknown'

        # Separate questions and answers based on language
        """
        bangla_questions = []
        transliterated_questions = []
        english_questions = []
        bangla_answers = []
        english_answers = []

        for _, row in data.iterrows():
            question = row['Questions']
            answer = row['Answers']

            # Detect the language for both question and answer
            language_question = detect_language(question)
            language_answer = detect_language(answer)

            if language_question == 'bn' and language_answer == 'bn':
                bangla_questions.append(question)
                bangla_answers.append(answer)
            elif language_question != 'en' and language_answer == 'bn':
                transliterated_questions.append(question)
                bangla_answers.append(answer)
            elif language_question == 'en' and language_answer == 'en':
                english_questions.append(question)
                english_answers.append(answer)

        # Print questions and answers by language category
        self.stdout.write(self.style.SUCCESS("Bangla Questions and Answers:"))
        for q, a in zip(bangla_questions, bangla_answers):
            language = "Bangla"
            entry = FinalDataset(question=q, answer=a, language=language)
            entry.save()
            self.stdout.write(f"Question: {q}, Answer: {a}, Language: {language}")

        self.stdout.write(self.style.SUCCESS("Transliterated Questions and Bangla Answers:"))
        for q, a in zip(transliterated_questions, bangla_answers):
            language = "Transliterated"
            entry = FinalDataset(question=q, answer=a, language=language)
            entry.save()
            self.stdout.write(f"Question: {q}, Answer: {a}, Language: {language}")

        self.stdout.write(self.style.SUCCESS("English Questions and Answers:"))
        for q, a in zip(english_questions, english_answers):
            language = "English"
            entry = FinalDataset(question=q, answer=a, language=language)
            entry.save()
            self.stdout.write(f"Question: {q}, Answer: {a}, Language: {language}")

        # Print the FinalDataset table
        self.stdout.write(self.style.SUCCESS("FinalDataset Table:"))
        final_dataset_entries = FinalDataset.objects.all()
        for entry in final_dataset_entries:
            self.stdout.write(f"Question: {entry.question}, Answer: {entry.answer}, Language: {entry.language}")

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
        """
        for _, row in data.iterrows():
            bangla_ques = row['bangla_ques'].split('\n')[0]
            transliterated_ques = row['transliterated_ques'].split('\n')[0]
            bangla_ans = row['bangla_ans']
            english_ques = row['english_ques'].split('\n')[0]
            english_ans = row['english_ans']
            entry = FinalDataset(
                bangla_ques=bangla_ques,
                transliterated_ques=transliterated_ques,
                bangla_ans=bangla_ans,
                english_ques=english_ques,
                english_ans=english_ans,
            )
            entry.save()
