from django.db import models
# from .question_answer import (Question, Answer)
# from django.contrib.auth.models import User


class QADataset(models.Model):
    bangla_ques = models.CharField(max_length=255, verbose_name='Bangla Question')
    english_ques = models.CharField(max_length=255, verbose_name='English Question')
    transliterated_ques = models.CharField(max_length=255, verbose_name='Transliterated (Banglish) Question')
    bangla_ans = models.CharField(max_length=255, verbose_name='Bangla Answer')
    english_ans = models.CharField(max_length=255, verbose_name='English Answer')
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)
    flags = models.BooleanField(default=False)
