from django.contrib import admin
from .models import Printer, Check

admin.site.site_header = "Админка тестового задания"
admin.site.index_title = "Администрирование"


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')
    list_filter = ('name',)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer_id', 'type', 'order', 'status', 'pdf_file')
    list_filter = ('printer_id', 'type', 'status')
    # readonly_fields = ('order', 'pdf_file')
    list_per_page = 10


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
