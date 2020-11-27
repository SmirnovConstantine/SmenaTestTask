import django_rq
import requests
import json
from .utils import CommonUtils
from .models import Check


url = 'http://0.0.0.0:32768/'

headers = {
    'Content-Type': 'application/json',    # This is important
}


def generate_pdf_for_checks():
    """ Генерируем pdf файлы для всех чеков, со статусом new """
    errors = CommonUtils()
    try:
        all_checks = Check.objects.all().filter(status="n")
        for check in all_checks:
            if check.type == "K":
                checkPath = '../templates/kitchen_check.html'
                typeCheck = 'kitchen'
            elif check.type == "C":
                checkPath = '../templates/client_check.html'
                typeCheck = 'client'

            # Обновляем статус чека, на render - и создаем pdf файл
            Check.objects.filter(id=check.id).update(status='r')

            data = {
                'contents': open(checkPath).read().encode('base64'),
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)

            with open('../media/pdf/{0}_{1}}.pdf'.format(check.order["id"], typeCheck), 'wb') as f:
                f.write(response.content)
    except Exception:
        return errors.errorResponse("чеки не найдены")

