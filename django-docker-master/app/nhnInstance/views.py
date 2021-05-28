from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from nhnInstance.models import Instance
from nhnInstance.serializers import InstanceSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def instance_list(request):
    if request.method == 'GET':
        instances = Instance.objects.all()

        instances_serializer = InstanceSerializer(instances, many=True)
        return JsonResponse(instances_serializer.data, safe=False)

    elif request.method == 'POST':
        instance_data = JSONParser().parse(request)
        instance_serializer = InstanceSerializer(data=instance_data)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_data, status=status.HTTP_201_CREATED)
        return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Instance.objects.all().delete()
        return JsonResponse({'message': '{} instances were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)

