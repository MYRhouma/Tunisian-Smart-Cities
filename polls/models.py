from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.contrib.auth
from account.models import Organisme


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Answer(models.Model):
    organisme = models.ForeignKey(Organisme, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.organisme)+' voted for "'+str(self.choice)+'".'



