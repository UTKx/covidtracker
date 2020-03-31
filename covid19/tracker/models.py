from django.db import models

# Create your models here.

class covid_world(models.Model):
    stat_id = models.AutoField(primary_key=True)
    total_cases = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()

    def __str__(self):
        return self.world_stats

class active_cases(models.Model):
    a_id = models.AutoField(primary_key=True)
    active_cases = models.IntegerField()
    mild_cases = models.IntegerField()
    critical_cases = models.IntegerField()

    def __str__(self):
        return self.active_cases

class closed_cases(models.Model):
    c_id = models.AutoField(primary_key=True)
    outcome = models.IntegerField()
    discharged = models.IntegerField()
    dead = models.IntegerField()

    def __str__(self):
        return self.closed_cases