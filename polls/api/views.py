from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer
from ..models import Poll, Choice, Vote

class TopicViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=True, methods=['get'], serializer_class=ChoiceSerializer)
    def choices(self, request, pk=None):
        poll = self.get_object()
        choices = Choice.objects.filter(poll=poll)
        serializer = self.get_serializer(choices, many=True)
        return Response(serializer.data) 

    @choices.mapping.post
    def post_choice(self, request, pk=None):
        data = request.data
        data['poll'] = pk

        serializer = ChoiceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class ChoiceViewSet(ModelViewSet): 
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    @action(detail=True, methods=['get'], serializer_class=VoteSerializer, permission_classes=[IsAuthenticatedOrReadOnly])
    def votes(self, request, pk=None):
       choice = self.get_object()
       votes = Vote.objects.filter(choice=choice)
       serializer = self.get_serializer(votes, many=True)
       return Response(serializer.data)

    @votes.mapping.post
    def post_vote(self, request, pk=None):
        user = request.user
        choice = self.get_object()

        if not Vote.objects.filter(user=user, choice=choice).exists(): # possible optimize this by creating voters field in choice model 
            data = request.data
            data['choice'] = pk

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)