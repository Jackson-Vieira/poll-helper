from shelve import Shelf
from django.db import models
from django.db.models.aggregates import Avg, Sum, Count, Min, Max
from django.contrib.auth.models import User

from datetime import datetime

import uuid

class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    poll_name = models.CharField(max_length=200, blank=False, null=False)

    randomize_choice_order = models.BooleanField(default=True, null=False)

    POLL_TYPES = (
    ('private', 'Private'),
    )

    poll_type = models.CharField(max_length=250, null=False, default='private', choices = POLL_TYPES)

    # path to download poll information
    poll_info_url = models.URLField(max_length=300, null=True, blank=True)

    # CACHEs (result, choices)

    # allow votes?
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

    # @classmethod
    # def winner(cls, question, result, num_cast_votes):
    #     pass

    @classmethod
    def get_url_info__by_uuid(cls, uuid):
        return cls.objects.get(id=uuid)

    def create_choice(cls):
        pass

    def voting_has_started(self):
        pass

    def voting_has_stopped(self):
        pass

    @property
    def get_choices(self):
        return self.choices.all() # BAD OTIMIZED

    @property
    def total_votes(self):
        return self.choices.all().aggregate(votes=Sum('votes')) # BAD OTIMIZED

    @property
    def get_results(self):
        return self.choices.all().annotate(votes=Sum('choices_votes')).order_by('-') #BAD OTIMIZED

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
        pass

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

class Vote(models.Model):
    user =  models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='registry', blank=False, null=False)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING, related_name='registry', blank=False, null=False)
    created = created = models.DateTimeField('creation date', auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Registry'
        verbose_name_plural = 'Registrys'
    
# class ElectionLog(models.Model):