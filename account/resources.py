from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import NotFound
from restless.exceptions import BadRequest
from restless.resources import skip_prepare
from restless.exceptions import Unauthorized

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from account.models import Pin
from account.models import Location
from account.models import SessionToken


#################################
# Generic and Base Resources    #
#################################

class BaseResource(DjangoResource):
    """
    Basic Resource definition. Aggregates a set of
    helper methods.
    """
    def prepare_list(self, queryset):
        l = []
        for item in queryset:
            l.append(self.prepare(item))
        return l

    def validate_fields(self, fields):
        if self.data.__class__ == list:
            raise BadRequest('No data sent!')
        data = {}
        for field in fields:
            if not self.data.get(field, None):
                raise BadRequest('Missing field "{}" on request.'.format(
                    field))
            data[field] = self.data.get(field)
        return data


#####################################
# Point of Sale Resources           #
#####################################


class POSAuthResource(BaseResource):
    """
    Resource that handles clerk authentication
    on mobile and web requests from Point of Sale.
    """
    def __init__(self, *args, **kwargs):
        super(POSAuthResource, self).__init__(*args, **kwargs)
        self.http_methods.update({
            'delete': {
                'DELETE': 'delete',
            }
        })

    def is_authenticated(self):
        return True

    def create(self):
        data = self.validate_fields([
            'email',
            'password',
        ])
        try:
            email = data.get('email', '').lower()
            user = User.objects.get(email__exact=email)
        except:
            raise Unauthorized("Invalid email address or password!")

        # check if its credentials are correct
        username = user.username
        user = authenticate(username=username, password=data['password'])
        if user and user.is_active and user.is_staff:
            # check if its already logged in, and delete previous session
            try:
                token = SessionToken.objects.get(user=user)
                token.delete()
            except SessionToken.DoesNotExist:
                pass
            # logs into a new session
            token = SessionToken(user=user)
            token.save()
            role = None
            if user.groups.count() > 0:
                role = user.groups.first().name
            locations = [l.serialize() for l in user.locations.all()]
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': role,
                'email': user.email,
                'token': token.value,
                'locations': self.prepare_list(locations)
            }
        # else, raise Unauthorized
        raise Unauthorized()

    def delete(self, pk):
        try:
            token = SessionToken.objects.get(value=pk)
            token.delete()
        except SessionToken.DoesNotExist:
            pass
        return {
            'status': 'ok'
        }

    def detail(self, pk):
        if self.request.user.is_authenticated():
            user = self.request.user
            locations = [l.serialize() for l in user.locations.all()]
            role = user.groups.first().name if user.groups.count() > 0\
                else None
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': role,
                'email': user.email,
                'locations': self.prepare_list(locations)
            }
        # if not logged in, return failure
        raise NotFound("Not logged in!")


class POSSecureResource(BaseResource):
    """
    Abstract resource that implements security level for
    all Point of Sale resources.
    """

    def is_authenticated(self):
        token = self.request.GET.get('token', None)
        if not token:
            return False
        try:
            session = SessionToken.objects.get(value=token)
        except SessionToken.DoesNotExist:
            return False
        return session is not None


class POSPinResource(POSSecureResource):
    """
    Handles PIN creation, removal and cashout process.
    """

    def __init__(self, *args, **kwargs):
        super(POSPinResource, self).__init__(*args, **kwargs)
        self.http_methods.update({
            'cashout': {
                'GET': 'cashout',
            }
        })

    preparer = FieldsPreparer(fields={
                              'number': 'number',
                              'credits': 'credits',
                              'status': 'status',
                              'location': 'location.id'
                              })

    def list(self, location):
        return Pin.objects.filter(location__id__exact=location,
                                  status__in=['new', 'active', 'cashout'])

    def detail(self, pk):
        return Pin.objects.get(number=pk)

    def create(self):
        self.validate_fields([
            'credits',
            'location'
        ])
        try:
            l = Location.objects.get(pk=self.data['location'])
        except Location.DoesNotExist:
            raise NotFound("Current site or location does not exists!")
        p = Pin(credits=self.data['credits'],
                location=l)
        p.save()
        return p

    @skip_prepare
    def delete(self, pk):
        try:
            pin = Pin.objects.get(number=pk)
        except Pin.DoesNotExist:
            raise NotFound("Pin number not found!")
        if pin.status != 'new':
            raise BadRequest("Cannot remove used Pin numbers!")
        pin.delete()
        return {
            "message": "Pin removed successfully!"
        }

    def cashout(self, pk):
        try:
            p = Pin.objects.get(number=pk)
        except Pin.DoesNotExist:
            raise NotFound("Pin number does not exists!")
        if p.status == 'active':
            p.status = 'cashout'
        elif p.status == 'cashout':
            p.status = 'redeemed'
        else:
            raise BadRequest("Cannot cashout a ticket in status '{}'.".format(
                p.status
            ))
        p.save()
        return p
