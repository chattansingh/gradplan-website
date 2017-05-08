from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class MajorRoadMaps(models.Model):
    major = models.CharField(max_length=200)
    road_map = JSONField()

    def __str__(self):
        return self.major
