from django.db import models



class Status(models.Model):
    """Модель статусов (загружено, обрабатывается, обработано)"""
    name_status = models.CharField(max_length=15)

    def __str__(self):
        return self.name_status



class File(models.Model):
    """Модель файла"""
    file = models.FileField(verbose_name='Файл')
    date_time_download = models.DateTimeField(auto_now_add=True)
    date_time_end_processing = models.DateTimeField(null=True, blank=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    resalt = models.CharField(max_length=15, null=True, default=None)
