from rest_framework.routers import SimpleRouter
from ..views import TopicViewSet, ChoiceViewSet

router = SimpleRouter()
router.register('topics', viewset=TopicViewSet)
router.register('choices', viewset=ChoiceViewSet)