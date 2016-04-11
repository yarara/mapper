from django.db import models


class Event(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True)
    event_id = models.SmallIntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True)
    age_restricted = models.CharField(max_length=255, blank=True)
    event_type = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    runtime = models.SmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    text = models.TextField(blank=True)
    place = models.CharField(max_length=255, blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    event_url = models.CharField(max_length=500, blank=True)
    chargeable_event = models.BooleanField()


class Places(models.Model):
    place_id = models.SmallIntegerField(null=True, blank=True)
    place_type = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    phones = models.CharField(max_length=255, blank=True)
    work_time_kassa = models.CharField(max_length=255, blank=True)
    work_time_openhours = models.CharField(max_length=255, blank=True)
    metro = models.CharField(max_length=255, blank=True)
    place_url = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
