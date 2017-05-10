from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

class SubjectInterests(models.Model):
    interest = models.IntegerField(blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_major = models.TextField(max_length=500, blank=True)
    base_graduation_plan = JSONField(blank=True, null=True)
    current_graduation_plan = JSONField(blank=True, null=True)
    current_semester = JSONField(blank=True, null=True)
    classes_taken = JSONField(blank=True, null=True)
    subject_interests = models.ManyToManyField(SubjectInterests, blank=True)
    progress = models.IntegerField(blank=True, default=0)
    common_classes = JSONField(blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()