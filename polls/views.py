from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .api.serializers import PollSerializer, ChoiceSeriliazer, VoteSerializer
from .models import Poll, Choice, Vote

class TopicViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=True, methods=['get'])
    def choices(self, request, pk=None):
       poll = self.get_object()
       choices = Choice.objects.filter(poll=poll)
       serializer = ChoiceSeriliazer(choices, many=True)
       return Response(serializer.data) 

class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSeriliazer
    
    @action(detail=True, methods=['get'])
    def registrys(self, request, pk=None):
       choice = self.get_object()
       registrys = Vote.objects.filter(choice=choice)
       serializer = VoteSerializer(registrys, many=True)
       return Response(serializer.data)

    @registrys.mapping.post
    def post_registry(self, request, pk=None):
        data = request.data
        data['user'] = request.user
        
        registry = VoteSerializer(data=data)
        if registry.is_valid():
            registry.save()
            return Response(registry.data, status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
"""class RegistryViewSet(ModelViewSet):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer
    """
