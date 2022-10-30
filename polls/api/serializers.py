from rest_framework.serializers import ModelSerializer
from ..models import Poll, Choice, Vote

class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = ('owner', 'poll_name')
        read_only_fields = ('id', 'created', 'updated',)

class ChoiceSeriliazer(ModelSerializer):
    
    # votes = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = '__all__'
        
class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ('user', 'choice', 'created')  
        extra_kwargs = {
            'user':'read_only',
        }