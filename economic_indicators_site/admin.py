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

@admin.register(models.CompanySystemUser)
class SystemAdmin(admin.ModelAdmin):
    list_filter = ('user',)

@admin.register(models.FixedAssets)
class AssetsAdmin(admin.ModelAdmin):
    list_filter = ('identifier',)


# admin.site.register(CompanyAdmin)
