from rest_framework.serializers import ModelSerializer
from ..models import Poll, Choice, Vote

class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'poll', 'choice_text', 'num_votes',)

class PollSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = (
            'id','owner', 'poll_name', 'randomize_choice_order', 'num_choices_max', 'poll_type', 'openvot', 'voting_starts_at', 'voting_ends_at', 'voting_started_at', 'voting_ended_at',
            'total_votes', 
            'choices'
            )
        read_only_fields = ('id', 'created', 'updated',)

class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ('user', 'choice', 'created', )  
        extra_kwargs = {
            'user':'read_only',
        }