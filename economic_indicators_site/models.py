from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=150, blank=False)
    company_nip = models.CharField(max_length=10)
    company_regon = models.CharField(max_length=14, blank=False)

    def __str__(self):
        return self.company_name


class SystemUser(User):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class CompanySystemUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


#TODO
# Supplement FullRaport model
class FullRaport(models.Model):
    pass

