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
    


# class QADataset(models.Model):
#     bangla_ques = models.ForeignKey(Question, related_name='bangla_ques', verbose_name='Bangla Question',
#                                     on_delete=models.DO_NOTHING, null=True)
#     english_ques = models.ForeignKey(Question, related_name='english_ques', verbose_name='English Question',
#                                      on_delete=models.DO_NOTHING, null=True)
#     transliterated_ques = models.ForeignKey(Question, related_name='transliterated_ques',
#                                             verbose_name='Transliterated (Banglish) Question',
#                                             on_delete=models.DO_NOTHING, null=True)
#     bangla_ans = models.ForeignKey(Answer, related_name='bangla_ans', verbose_name='Bangla Answer',
#                                    on_delete=models.DO_NOTHING, null=True)
#     english_ans = models.ForeignKey(Answer, related_name='english_ans', verbose_name='English Answer',
#                                     on_delete=models.DO_NOTHING, null=True)
#     created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
#     update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)
