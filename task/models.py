from django.db import models
import jsonfield

CHECK_TYPES = (
    ('K', 'kitchen'),
    ('C', 'client'),
)


class Printer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название пинтера")
    api_key = models.CharField(max_length=255, verbose_name="Ключ доступа к API", unique=True, null=False, blank=False,
                               db_index=True)
    check_type = models.CharField(max_length=1, choices=CHECK_TYPES, verbose_name="Тип чека")
    point_id = models.IntegerField()

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"

    def __str__(self):
        return self.name


class CheckManager(models.Manager):
    """ Создание чека """
    def create_check(self, printer_id, type, order, status):
        check = self.create(printer_id=printer_id, type=type, order=order, status=status)
        return check


class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name="Принтер", blank=False, null=False,
                                   related_name="printers", db_index=True)
    type = models.CharField(max_length=1, choices=CHECK_TYPES, verbose_name="Тип чека")
    order = jsonfield.JSONField(verbose_name="Информация о заказе")
    STATUS_TYPE = (
        ('n', 'new'),
        ('r', 'rendered'),
        ('p', 'printed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPE, verbose_name="Статус чека")
    pdf_file = models.FileField(null=True, blank=True, verbose_name="Ссылка на созданный файл")

    objects = CheckManager()

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
