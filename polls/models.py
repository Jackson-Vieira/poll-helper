from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=False)


    def was_published_recently(self):
        datetime_now = timezone.now()
        return datetime_now - datetime.timedelta(days=1) <= self.pub_date <= datetime_now
    
    def there_choice(self):
        return len(self.choice_set.all()) >= 1

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.choice_text

    class Meta:
        ordering = ["-votes"]