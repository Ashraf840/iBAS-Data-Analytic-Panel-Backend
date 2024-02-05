from django.db import models

class FinalDataset(models.Model):
    bangla_ques = models.TextField(default='')  
    transliterated_ques = models.TextField(default='')  
    bangla_ans = models.TextField(default='')  
    english_ques = models.TextField(default='')
    english_ans = models.TextField(default='')
    TRAINED = 'Trained'
    UNTRAINED = 'Untrained'
    STATUS_CHOICES = [
        (TRAINED, 'Trained'),
        (UNTRAINED, 'Untrained'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=UNTRAINED, 
        db_index=True
    )