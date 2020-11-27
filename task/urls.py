from django.conf.urls import url
from .views import create_checks, new_checks, get_pdf_for_check

urlpatterns = [
    url(r'^create_checks/', create_checks),
    url(r'^new_checks/?(?:api_key=(?P<api_key>[\w-]+)?/)$', new_checks),
    url(r'^check/(?:api_key=(?P<api_key>[\w-]+)?&(?:check=(?P<check>[\d]+)?))/$', get_pdf_for_check),
]
