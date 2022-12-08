from rest_framework.serializers import ModelSerializer
from ..models import Poll, Choice, Vote

class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'poll', 'choice_text', 'num_votes',)

        read_only_fields = ('id', 'num_votes')
        #extra_kwargs = {}

class PollSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Poll
        fields = (
            'id', 'owner', 'poll_name', 'randomize_choice_order', 'num_choices_max', 'poll_type', 'openvot', 'voting_starts_at', 'voting_ends_at', 'voting_started_at', 'voting_ended_at',
            'total_votes', 
            'choices'
            )
        read_only_fields = ('id', 'owner' 'created', 'updated', 'total_votes',)
        #extra_kwargs = {}

class VoteSerializer(ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Vote
        fields = ('user', 'choice', 'created')  
        read_only_fields = ('user', 'created',)
        #extra_kwargs = {}