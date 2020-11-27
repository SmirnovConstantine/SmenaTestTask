from django.http import HttpResponse, JsonResponse
from .models import Printer, Check
from django.views.decorators.csrf import csrf_exempt
from .rqTask import generate_pdf_for_checks

import json
import django_rq
from collections import Counter


from .utils import CommonUtils


errors = CommonUtils()


@csrf_exempt
def create_checks(request):
    """ Ф-ция создания чеков """
    if request.method == 'POST':
        # преобразуем bytes в словарь
        my_json = request.body.decode('utf8').replace("'", '"')
        data = json.loads(my_json)

        if data.get("point_id"):
            try:
                Printer.objects.all().filter(point_id=data.get["point_id"])
            except Exception:
                return errors.errorResponse("для данной точки не настроено ни одного принтера")
            else:
                return is_all_checks(data)
    else:
        return errors.errorResponse("method not allowed")


def is_all_checks(data):
   # Проверяем созданы ли чеки, и ели да, то сколько созданно, чтобы дальше созать чеки
    order_ids = get_order_ids()
    count_order_checks = Counter(order_ids)
    if (data.get("id") in order_ids) and (count_order_checks[data.get("id")] == 2):
        return errors.errorResponse("для данного заказа уже созданы чеки")
    elif count_order_checks[data.get("id")] == 1:
        return HttpResponse("Need one check")
    else:
        return push_checks(data)


def push_checks(data):
    """ Создание клиентского и кухонного чеков """
    try:
        printers = Printer.objects.all().filter(point_id=data["point_id"])
    except Exception:
        return errors.errorResponse("ненастроен принтер")
    else:
        for printer in printers:
            Check.objects.create_check(printer, 'C', data, 'n')
            Check.objects.create_check(printers, 'K', data, 'n')
        django_rq.enqueue(generate_pdf_for_checks)  # Генерируем pdf-файлы
        return JsonResponse({
            "ok": "Чеки успешно созданы"
        })


def get_order_ids():
    """ получаем id всех заказов, для которых уже есть чеки"""
    all_checks = Check.objects.all()
    order_ids = []
    for orders_id in all_checks:
        order_ids.append(orders_id.order["id"])
    return order_ids


def new_checks(request, **kwargs):
    """ Метод получения чеков для принтера """
    if request.method == 'GET':
        checks_ids = []
        try:
            printer = Printer.objects.get(api_key=kwargs['api_key'])
            checks = Check.objects.all().filter(printer_id=printer).filter(status="r")  # Получаем сформированные чеки
            for check in checks:
                checks_list = {"id": check.id}
                checks_ids.append(checks_list)
            return JsonResponse({
                "checks": checks_ids
            })
        except Exception:
            return errors.errorResponse("ошибка авторизации")
    else:
        return errors.errorResponse("method not allowed")


def get_pdf_for_check(request, **kwargs):
    """ Метод получения pdf-файла для чека """
    if request.method == 'GET':
        try:
            printer = Printer.objects.get(api_key=kwargs['api_key'])
        except Exception:
            return errors.errorResponse("ошибка авторизации")
        try:
            checks = Check.objects.all().filter(printer_id=printer).filter(id=kwargs['check'])
            Check.objects.filter(id=kwargs['check']).update(status='p')  # Обновляем статус на printed
        except Exception:
            return errors.errorResponse("данного чека не существует")
        return checks[0].pdf_file
