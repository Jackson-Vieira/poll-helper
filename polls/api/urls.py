from rest_framework.routers import SimpleRouter
from ..views import TopicViewSet, ChoiceViewSet

router = SimpleRouter()
router.register('polls', viewset=TopicViewSet)
router.register('choices', viewset=ChoiceViewSet)