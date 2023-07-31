from django.db import models


class Language(models.Model):
    language_name = models.CharField(verbose_name='Language Name', max_length=100, unique=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def __str__(self):
        return f'Language: {self.language_name}'
