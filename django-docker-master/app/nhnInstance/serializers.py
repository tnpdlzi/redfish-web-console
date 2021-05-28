from rest_framework import serializers
from nhnInstance.models import Instance


class InstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instance
        fields = ('name',
                  'ip',
                  'os',
                  'iType',
                  'keyPair',
                  'area',
                  'status')
