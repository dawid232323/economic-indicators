from django.contrib import admin

from . import models

"""

dawidpylak
password

"""


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ('company_name',)


# admin.site.register(CompanyAdmin)
