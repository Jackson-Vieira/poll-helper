from django.db import models
from django.contrib.auth.models import User

import uuid

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    topic_text = models.CharField(max_length=200, blank=False, null=False)
    created = models.DateTimeField('creation date', auto_now_add=True)
    updated = models.DateField('last update date', auto_now=True)

    def there_choice(self):
        return len(self.choice_set.all()) >= 1

    def __str__(self):
        return self.question_text
    
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['topic_text']

class Choice(models.Model):
    question = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='question', blank=False, null=False)
    choice_text = models.CharField(max_length=200, blank=False, null=False)
    registrys = models.ManyToManyField(User, through='Registry', related_name='registrys')
    # votes = models.IntegerField(default=0) #  Change to ONE-TO-MANY
    # image 

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        
class Registry(models.Model):
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='registry', blank=False, null=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='registry', blank=False, null=False)
    created = created = models.DateTimeField('creation date', auto_now_add=True)

    class Meta:
        verbose_name = 'Registry'
        verbose_name_plural = 'Registrys'