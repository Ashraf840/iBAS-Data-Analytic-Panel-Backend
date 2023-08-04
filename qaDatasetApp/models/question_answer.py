from django.db import models
from django.contrib.auth.models import User
from .language import Language
from django.shortcuts import get_object_or_404


class Answer(models.Model):
    answer = models.TextField(verbose_name='Answer')
    language = models.ForeignKey(Language, related_name='ans_lang_name', on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return f'Answer: {self.answer}'

    @staticmethod
    def get_object(*args, **kwargs):
        if kwargs.get('answer') is not None:
            # [Resource of 'get_object_or_404']
            #   https://www.fullstackpython.com/django-shortcuts-get-object-or-404-examples.html
            return get_object_or_404(Answer, answer=kwargs.get('answer'))


class Question(models.Model):
    question = models.TextField(verbose_name='Question')
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return f'Question: {self.question}'

