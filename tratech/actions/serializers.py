from rest_framework import serializers
from actstream.models import Action

class ActionSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.name', read_only=True)
    target_name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ['id', 'actor_name', 'verb', 'target_name', 'timestamp']

    def get_target_name(self, obj):
        if obj.target:
            return getattr(obj.target, 'name', str(obj.target))
        return None