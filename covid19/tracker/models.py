from django.db import models

# Create your models here.

class covid_world(models.Model):
    stat_id = models.AutoField(primary_key=True)
    total_cases = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()

    def __str__(self):
        return self.world_stats