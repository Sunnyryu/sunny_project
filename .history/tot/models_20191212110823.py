from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Keyword(models.Model):
    word = models.CharField(max_length=30)
    date = models.DateField()
    high_word_frequency = JSONField(default={}, dump_kwargs={'ensure_ascii': False})
