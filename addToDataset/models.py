from django.db import models

class SuggestiveQuestions(models.Model):
    text = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    marked_for_removal = models.BooleanField(default=False)
    def __str__(self):
        return self.text