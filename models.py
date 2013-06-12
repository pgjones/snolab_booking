from django.db import models

class Apartment(models.Model):
    """ Apartments have many beds."""
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    address_zip = models.CharField(max_length=20)
    address_city = models.CharField(max_length=200)
    contact = models.EmailField(max_length=254) # 254 is recommended in docs
    information = models.TextField(blank=True) # Extra details
    short_name = models.CharField(max_length=10) # Short descriptor
    experiment = models.CharField(max_length=200)
    def __unicode__(self):
        return self.short_name

BED_TYPE = ( ("DOUBLE", "Double"),
             ("SINGLE", "Single"),
             ("FUTON", "Futon") )

class Bed(models.Model):
    """ Beds can be booked."""
    apartment = models.ForeignKey(Apartment)
    number = models.IntegerField()
    type = models.CharField(max_length=6, choices=BED_TYPE)
    information = models.TextField(blank=True) # Extra details
    def __unicode__(self):
        return self.apartment.short_name + " bed " + str(self.number)

class Visit(models.Model):
    """ A visit to SNOLAB."""
    contact = models.EmailField(max_length=254) # 254 is recommended in docs
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    experiment = models.CharField(max_length=200)
    def __unicode__(self):
        return '%s: %s to %s' % (self.contact, self.check_in.date(), self.check_out.date())

class Booking(models.Model):
    """ A booking of a bed."""
    bed = models.ForeignKey(Bed)
    visit = models.ForeignKey(Visit)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    booking_date = models.DateTimeField()
    def __unicode__(self):
        return '%s: %s to %s' % (self.bed, self.check_in.date(), self.check_out.date())

