from django.db import models
from .question_answer import (Question, Answer)
from django.contrib.auth.models import User


class QADataset(models.Model):
    bangla_ques = models.ForeignKey(Question, related_name='bangla_ques', verbose_name='Bangla Question',
                                    on_delete=models.DO_NOTHING)
    english_ques = models.ForeignKey(Question, related_name='english_ques', verbose_name='English Question',
                                     on_delete=models.DO_NOTHING)
    transliterated_ques = models.ForeignKey(Question, related_name='transliterated_ques',
                                            verbose_name='Transliterated (Banglish) Question',
                                            on_delete=models.DO_NOTHING)
    bangla_ans = models.ForeignKey(Answer, related_name='bangla_ans', verbose_name='Bangla Answer',
                                   on_delete=models.DO_NOTHING)
    english_ans = models.ForeignKey(Answer, related_name='english_ans', verbose_name='English Answer',
                                    on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)
