from rest_framework import serializers
from restApi.models import Servers


# class TutorialSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Tutorial
#         fields = ('id',
#                   'title',
#                   'description',
#                   'published')
#
# class MembersSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Members
#         fields = ('idUrl')


class ServersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servers
        fields = (
                    'ip',
                    'username',
                    'password',
                    'grafanaId',
                    'grafanaUid',
                    'tempThreshold',
                    'powerThreshold',
                    'cdate')


