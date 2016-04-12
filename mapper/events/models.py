from django.db import models


class Place(models.Model):
    place_type = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    phones = models.CharField(max_length=255, blank=True)
    work_time_kassa = models.CharField(max_length=255, blank=True)
    work_time_openhours = models.CharField(max_length=255, blank=True)
    metros = models.CharField(max_length=255, blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)


class Event(models.Model):
    title = models.CharField(max_length=255, blank=True)
    age_restricted = models.CharField(max_length=255, blank=True)
    event_type = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    persons = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    text = models.TextField(blank=True)
    stage_theatre = models.CharField(max_length=255, blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    price = models.BooleanField()
    places = models.ManyToManyField('Place', related_name='events', null=True, blank=True,
                                    through='Schedule')


class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=10)
    timetill = models.CharField(max_length=10, null=True, blank=True)
