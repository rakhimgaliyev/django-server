import json
from unicodedata import decimal

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from backend_diploma.models import Point, Position, Data
from backend_diploma.serializers import PointSerializer
from utils.algos import algos


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_map(request):
    data = request.data

    Position.objects.all().delete()
    Point.objects.all().delete()

    for point in data:
        position = point['position']
        clusters = point.get('clusters')
        if clusters:
            Data.objects.all().delete()
            Data.objects.create(clusters=clusters)

        position_model = Position.objects.create(x=position['x'], y=position['y'])

        Point.objects.create(id=point['id'], description=point['description'], position=position_model)

    return Response(status=status.HTTP_200_OK)


def _decode(o):
    # Note the "unicode" part is only for python2
    if isinstance(o, str):
        try:
            return float(o)

        except ValueError:
            return o
    elif isinstance(o, dict):
        return {k: _decode(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_decode(v) for v in o]
    else:
        return o


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_clusters(request):
    serializer = PointSerializer(Point.objects.all(), many=True)

    data = json.loads(json.dumps(serializer.data), object_hook=_decode)
    clusters = Data.objects.first().clusters
    data.append({
        "clusters": clusters,
    })

    return Response(algos(data))