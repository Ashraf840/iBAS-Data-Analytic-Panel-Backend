from django.contrib import admin
from .models import (
    language as language_model,
    question_answer as question_answer_model,
    qa_dataset as qa_dataset_model)
from .admin_panel_uis import (language, question_answer, qa_dataset)


admin.site.register(language_model.Language, language.LanguageAdmin)
admin.site.register(question_answer_model.Answer, question_answer.AnswerAdmin)
admin.site.register(question_answer_model.Question, question_answer.QuestionAdmin)
admin.site.register(qa_dataset_model.QADataset, qa_dataset.QADatasetAdmin)
