import pandas as pd
from openpyxl import load_workbook
from langdetect import detect
from .models import FinalDataset

# Define a function to detect the language
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'Unknown'

# Load the Excel file
excel_file = '/home/user/Workstation/ibas-chat-operator/ibas-data-analytics-panel-backend/ibas_final_dataset.xlsx'

# Load the data from the Excel file
data = pd.read_excel(excel_file, engine='openpyxl')

# Separate questions and answers based on language
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
print("Bangla Questions and Answers:")
for q, a in zip(bangla_questions, bangla_answers):
    print(f"Question: {q}, Answer: {a}, Language: Bangla")
    language = "Bangla"
    entry = FinalDataset(question=q, answer=a, language=language)
    entry.save()


print("\nTransliterated Questions and Bangla Answers:")
for q, a in zip(transliterated_questions, bangla_answers):
    print(f"Question: {q}, Answer: {a}, Language: Transliterated")
    language = "Transliterated"
    entry = FinalDataset(question=q, answer=a, language=language)
    entry.save()

print("\nEnglish Questions and Answers:")
for q, a in zip(english_questions, english_answers):
    print(f"Question: {q}, Answer: {a}, Language: English")
    language = "English"
    entry = FinalDataset(question=q, answer=a, language=language)
    entry.save()
