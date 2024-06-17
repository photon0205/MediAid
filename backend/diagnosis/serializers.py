from rest_framework import serializers

class SymptomSerializer(serializers.Serializer):
    symptoms = serializers.ListField(
        child=serializers.FloatField()
    )
