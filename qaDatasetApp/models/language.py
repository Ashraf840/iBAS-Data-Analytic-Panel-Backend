from django.db import models
from django.shortcuts import get_object_or_404


class Language(models.Model):
    language_name = models.CharField(verbose_name='Language Name', max_length=100)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return f'Language: {self.language_name}'

    @staticmethod
    def get_object(*args, **kwargs):
        if kwargs.get('language_name') is not None:
            # NB (kwargs.get('language_name')): "language_name" appears in the 'create()' method of 'Answer'
            # serializer's validated_data as an ordered-dcit, since the "Language" model's string representation returns
            # the "langauge_name" field.

            # [Resource of 'get_object_or_404']
            #   https://www.fullstackpython.com/django-shortcuts-get-object-or-404-examples.html
            return get_object_or_404(Language, language_name=kwargs.get('language_name'))
