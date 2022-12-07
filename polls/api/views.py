from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer
from ..models import Poll, Choice, Vote

class TopicViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=True, methods=['get'], serializer_class=ChoiceSerializer)
    def choices(self, request, pk=None):
        poll = self.get_object()
        choices = Choice.objects.filter(poll=poll)
        serializer = self.get_serializer(data=choices, many=True)
        return Response(serializer.data) 

    @choices.mapping.post
    def post_choice(self, request, pk=None):
        data = request.data
        
        if not data.get("poll"): # This does not work  
            data['poll'] = pk

        choice = ChoiceSerializer(data=data)
        if choice.is_valid():
            choice.save()
            return Response(choice.data, status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    
    @action(detail=True, methods=['get'], serializer_class=VoteSerializer)
    def votes(self, request, pk=None):
       choice = self.get_object()
       votes = Vote.objects.filter(choice=choice)
       serializer = self.get_serializer(votes, many=True)
       return Response(serializer.data)

    @votes.mapping.post
    def post_vote(self, request, pk=None):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)