from rest_framework import serializers

from handler import models


class StatusSerializer(serializers.ModelSerializer):
    """Вывод статуса файла"""
    class Meta:
        model = models.Status
        fields = ('name_status', )


class FileListSerializer(serializers.ModelSerializer):
    """Вывод списка файлов"""
    status = StatusSerializer(read_only=True)
    class Meta:
        model = models.File
        fields = ['id', 'file', 'date_time_download', 'status', ]


class FileDetailsSerialiser(serializers.ModelSerializer):
    """Вывод детальной информации о файле"""
    status = StatusSerializer()
    class Meta:
        model = models.File
        fields = '__all__'

