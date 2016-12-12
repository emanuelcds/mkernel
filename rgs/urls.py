from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from account.resources import POSAuthResource
from account.resources import POSPinResource

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/pos/auth/(?P<pk>[a-f0-9]+)/?',
        csrf_exempt(POSAuthResource.as_view('delete')), name='pos_logout'),
    url(r'^api/pos/auth/?', include(POSAuthResource.urls())),
    url(r'^api/pos/pin/location/(?P<location>\d+)/?',
        POSPinResource.as_list(), name='pos_pin_list'),
    url(r'^api/pos/pin/(?P<pk>\d+)/?',
        POSPinResource.as_detail(), name='pos_pin_detail'),
    url(r'^api/pos/pin/cashout/(?P<pk>\d+)/?',
        POSPinResource.as_view('cashout'), name='pos_pin_cashout'),
    url(r'^api/pos/pin/?', include(POSPinResource.urls())),
]
