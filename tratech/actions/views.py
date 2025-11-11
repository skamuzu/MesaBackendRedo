from rest_framework import generics
from actstream.models import Action
from .serializers import ActionSerializer
# Create your views here.

class ActionListView(generics.ListAPIView):
    queryset = Action.objects.select_related('actor-content_type', 'target-content_type').order_by('-timestamp')
    serializer_class = ActionSerializer