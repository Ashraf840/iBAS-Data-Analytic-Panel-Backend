from django.db import models


class FinalDataset(models.Model):
    bangla_ques = models.TextField(default='')
    transliterated_ques = models.TextField(default='')
    bangla_ans = models.TextField(default='')
    english_ques = models.TextField(default='')
    english_ans = models.TextField(default='')


"""
class FinalDataset(models.Model):
    question = models.TextField()  
    answer = models.TextField() 
    language = models.CharField(max_length=255)
"""
