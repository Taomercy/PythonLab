from rest_framework import serializers
from Web.models import Tar


class TarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tar
        fields = ('filename', 'abspath', 'uploader', 'upload_time')
