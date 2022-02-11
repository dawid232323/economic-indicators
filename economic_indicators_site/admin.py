from django.contrib import admin

from . import models

"""

dawidpylak
password


kowal
P@ssword23


dejf
@B@ndomand666

"""


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ('company_name',)


@admin.register(models.Assets)
class SystemAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.Liabilities)
class SystemAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.ProfitsLoses)
class ProfitAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


# admin.site.register(CompanyAdmin)
