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

    def save_model(self, request, obj, form, change, **kwargs):
        user = obj.created_by.user.username
        time_period = obj.time_period
        obj.save(user=user, time_period=time_period, **kwargs)



@admin.register(models.Liabilities)
class SystemAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.ProfitsLoses)
class ProfitAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.FullRaportBlock)
class RaportBlockAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.CompanySystemUser)
class CompanySystemUserAdmin(admin.ModelAdmin):
    list_filter = ('user', )


@admin.register(models.FinalRaport)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('created_by', )


@admin.register(models.RaportFileModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )


@admin.register(models.BusinessCharacteristicModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )


@admin.register(models.FullMarketAnalisisModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )


@admin.register(models.TypeOfEconomicActivityModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )

    def save_model(self, request, obj, form, change, **kwargs):
        user = obj.created_by.user.username
        obj.save(user=user, **kwargs)


@admin.register(models.ApplicantOfferOperationIncomeModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )


@admin.register(models.CurrentPlaceOnTheMarketModel)
class ComanyFullRaportAdmin(admin.ModelAdmin):
    list_filter = ('identifier', )
# admin.site.register(CompanyAdmin)
