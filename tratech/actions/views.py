from rest_framework import generics
from actstream.models import Action
from .serializers import ActionSerializer
from rest_framework.permissions import IsAuthenticated
from users.middleware import ClerkAuthentication
# Create your views here.

class ActionListView(generics.ListAPIView):
    queryset = Action.objects.select_related('actor_content_type', 'target_content_type').order_by('-timestamp')
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ClerkAuthentication]