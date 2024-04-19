from datetime import datetime

from openpyxl import Workbook
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet, Model
from django.contrib.admin import ModelAdmin


def export_as_excel(self, request, queryset: QuerySet):
    meta = self.model._meta
    response: HttpResponse = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Export_{datetime.now()}.xlsx'
    # field_names = [field.name for field in meta.fields]
    excel_title = [field.verbose_name for field in meta.fields]
    field_names = [field.name for field in meta.fields]
    wb = Workbook()
    ws = wb.active
    ws.append(excel_title)
    for obj in queryset:
        data = [f'{getattr(obj, field)}' for field in field_names]
        row = ws.append(data)
    wb.save(response)
    return response


# export_as_excel.short_description = '导出Excel'


def api_export_as_excel(self, request, queryset: QuerySet):
    meta: Model = self.get_object()._meta
    exclude: list[str] = self.exclude_export
    response: HttpResponse = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename=Export_{datetime.now()}.xlsx'
    # field_names = [field.name for field in meta.fields]
    excel_title = [field.verbose_name for field in meta.fields if field.name not in exclude]
    field_names = [field.name for field in meta.fields if field.name not in exclude]
    wb = Workbook()
    ws = wb.active
    ws.append(excel_title)
    ws.append(field_names)
    data = [f'{getattr(obj, field)}' for field in field_names for obj in queryset]
    ws.append(data)
    wb.save(response)
    return response
