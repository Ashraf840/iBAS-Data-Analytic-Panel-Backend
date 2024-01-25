from django.db import models

class FinalDataset(models.Model):
    bangla_ques = models.TextField(default='')  
    transliterated_ques = models.TextField(default='')  
    bangla_ans = models.TextField(default='')  
    english_ques = models.TextField(default='')
    english_ans = models.TextField(default='') 
