from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from backend_diploma.models import Point, Position
from backend_diploma.serializers import PointSerializer

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_map(request):
    data = request.data

    for point in data:
        position = point['position']
        position_model = Position.objects.create(x=position['x'], y=position['y'])

        Point.objects.create(id=point['id'], description=point['description'], position=position_model)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_clusters(request):
    serializer = PointSerializer(Point.objects.all(), many=True)
    return Response(serializer.data)