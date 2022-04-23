from rest_framework import serializers

from backend_diploma.models import Point, Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    position = PositionSerializer()

    class Meta:
        model = Point
        fields = '__all__'
