from django.db import models
from django.db.models.aggregates import Avg, Sum, Count, Min, Max
from django.contrib.auth.models import User
from django.utils import timezone 
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

class PollTypeChoices(models.TextChoices):
    private = 'Private' 
    public =  'Public' 

class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    poll_name = models.CharField(max_length=200, blank=False, null=False)

    randomize_choice_order = models.BooleanField(default=True, null=False)
    num_choices_max = models.PositiveIntegerField(
        default=10,
        validators=[
            MaxValueValidator(10), MinValueValidator(2)
            ])

    poll_type = models.CharField(max_length=250, null=False, default=PollTypeChoices.public, choices= PollTypeChoices.choices)

    openvot = models.BooleanField(default=False)

    created = models.DateTimeField('creation date', auto_now_add=True)
    updated = models.DateField('last update date', auto_now=True)

    # dates for the election steps, as scheduled
    voting_starts_at = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)
    voting_ends_at = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)

    # dates when things were forced to be performed
    voting_started_at = models.DateTimeField(auto_now_add=False, default=None, null=True)
    voting_ended_at = models.DateTimeField(auto_now_add=False, default=None, null=True)


    @property
    def metadata(self):
        return {
            'randomize_choice_order': self.randomize_choice_order,
      }

    @classmethod
    def get_url_info__by_uuid(cls, uuid):
        return cls.objects.get(id=uuid)

    def voting_has_started(self):
        current_time = timezone.now()
        return current_time >= self.voting_starts_at or current_time >= self.voting_started_at

    def voting_has_stopped(self):
        current_time = timezone.now()
        return current_time <= self.voting_end_at or current_time <= self.voting_ended_at

    @property
    def get_choices(self):
        choices = self.choices.all()
        return choices.values()

    @property
    def num_choices(self):
        self.choices.count()

    @property
    def total_votes(self):
        return self.choices.aggregate(total_votes=Count('votes'))['total_votes']

    @property
    def get_results(self):
        return self.choices.annotate(total=Count('votes__id')).order_by('-total')

    @property
    def type(self):
        return self.poll_type

    def __str__(self):
        return self.poll_name
    
    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'
        ordering = ['-created']

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices', blank=False, null=False)
    choice_text = models.CharField(max_length=200, blank=False, null=False)
    votes = models.ManyToManyField(User, through='Vote', related_name='votes')

    @property
    def num_votes(self):
        return self.votes.count()

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

class Vote(models.Model):
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='registry', blank=False, null=False)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING, related_name='registry', blank=False, null=False)
    created = models.DateTimeField('creation date', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'