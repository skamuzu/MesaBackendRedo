from actstream.models import Action
from rest_framework import serializers

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'actor', 'verb', 'target', 'timestamp',"message"]
        
        def get_message(self, obj):
            if obj.target:
                return f"{obj.actor} {obj.verb} {obj.target}"
            return f"{obj.actor} {obj.verb}"
            
    