from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    average_rating = models.IntegerField(blank=True, default=0)
    number_of_ratings = models.IntegerField(blank=True, default=0)
    total_rating = models.IntegerField(blank=True, default=0)
    # rmp = rate my professor
    rmp_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.first_name

class ClassRating(models.Model):
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    class_name = models.CharField(max_length=10)
    class_id = models.IntegerField(blank=True)
    number_rating = models.IntegerField(blank=True)
    rating = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return self.class_name
