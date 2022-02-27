from datetime import datetime
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from django.db import transaction


from handler import serializers
from handler import models
from handler import functions




class FileListView(generics.ListCreateAPIView):
    """Вывод список файлов"""
    serializer_class = serializers.FileListSerializer
    queryset = models.File.objects.all()


class FileDetailsView(views.APIView):
    """Вывод детальной информации о файле и запуск обработки"""
    def get(self, request, pk):
        queryset = models.File.objects.get(id=pk)
        serializer_for_queryset = serializers.FileDetailsSerialiser(instance=queryset)
        return Response(serializer_for_queryset.data)

    def put(self, request, pk):
        queryset = models.File.objects.get(id=pk)
        serializer_for_queryset = serializers.FileDetailsSerialiser(instance=queryset)
        if queryset.status.name_status == "loaded":
            with transaction.atomic():
                queryset.status = models.Status.objects.get(id=2)
                queryset.save()
            try:
                list_after, list_before = functions.xlsx_handler(queryset.file)
                list_after_handler = functions.list_handler(list_after)
                list_before_handler = functions.list_handler(list_before)
                if len(list_after_handler) > len(list_before_handler):
                    resalt_list = functions.list_comparison(list_after_handler, list_before_handler)
                    resalt = f'added: {resalt_list[0]}'
                else:
                    resalt_list = functions.list_comparison(list_before_handler, list_after_handler)
                    resalt = f'removed: {resalt_list[0]}'
            except Exception:
                resalt = 'В файле нужная информация не найдена'
            with transaction.atomic():
                queryset.date_time_end_processing = datetime.now()
                queryset.resalt = resalt
                queryset.status = models.Status.objects.get(id=3)
                queryset.save()
        return Response(serializer_for_queryset.data)

