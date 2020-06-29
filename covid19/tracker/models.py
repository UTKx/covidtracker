from django.db import models

# Create your models here.

class CovidWorld(models.Model):
    stat_id = models.AutoField(primary_key=True)
    total_cases = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()

class CovidCountry(models.Model):
    update_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100)
    total_cases = models.IntegerField()
    today_cases = models.IntegerField()
    total_deaths = models.IntegerField()
    today_deaths = models.IntegerField()
    recovered = models.IntegerField()
    active = models.IntegerField()
    critical = models.IntegerField()
    casepermillion = models.IntegerField()
    deathpermillion = models.IntegerField()
    tests = models.IntegerField()
    testpermillion = models.IntegerField()

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = 'Covid Countries'