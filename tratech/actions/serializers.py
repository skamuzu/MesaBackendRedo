from rest_framework import serializers
from actstream.models import Action


class ActionSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    target_name = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ["id", "actor_name", "verb", "target_name", "timestamp", "model_name" ]

    def get_target_name(self, obj):
        if obj.target:
            return getattr(obj.target, "name", str(obj.target))
        return None

    def get_actor_name(self, obj):
        actor = obj.actor

        if not actor:
            return None

        first_name = getattr(actor, "first_name", "")
        last_name = getattr(actor, "last_name", "")

        full_name = f"{first_name} {last_name}".strip()
        return full_name

    def get_model_name(self, obj):
        actor = obj.actor
        
        if not actor:
            return None
        return actor.__class__.__name__