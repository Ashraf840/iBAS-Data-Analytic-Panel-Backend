from django.db import models

class FinalDataset(models.Model):
    question = models.TextField()  
    answer = models.TextField() 
    language = models.CharField(max_length=255)
