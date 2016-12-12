import random

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """ Base Abstract Model """
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SessionToken(BaseModel):
    value = models.CharField(max_length=32, primary_key=True)
    user = models.OneToOneField(User, related_name='token')

    def save(self, *args, **kwargs):
        token_bits = random.getrandbits(128)
        self.value = "%032x" % token_bits
        super(SessionToken, self).save(*args, **kwargs)


class Location(BaseModel):
    """
    Name of locations and staff for each
    distributor's site.
    """
    name = models.CharField(max_length=100, blank=False,
                            unique=True)
    staff = models.ManyToManyField(User, related_name='locations')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active
        }

    class Meta:
        permissions = (
            ('clerk', 'Login as a Clerk on POS'),
        )


class Pin(BaseModel):
    """
    Model that holds a pin number and store
    the customer's wallet.
    """
    STATUS_CHOICES = (
        ('new', 'New'),
        ('active', 'Active'),
        ('cashout', 'Cash Out'),
        ('redeemed', 'Redeemed'),
        ('expired', 'Expired'),
    )
    number = models.CharField(max_length=6, blank=False, primary_key=True)
    credits = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='new')
    location = models.ForeignKey(Location, related_name="pins", null=False)

    def save(self, *args, **kwargs):
        if not self.number or self.number == "":
            self.number = self.generate_pin()
        super(Pin, self).save(*args, **kwargs)

    def generate_pin(self):
        random.seed()
        while True:
            pin = random.randint(1024, 999999)
            pin = "%06d" % (pin)
            try:
                Pin.objects.get(pk=pin)
            except Pin.DoesNotExist:
                break
        return pin
