from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from account.resources import POSAuthResource
from account.resources import POSPinResource
from slot import views as slot_views

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
    url(r'^api/pos/pin/?', include(POSPinResource.urls())),
    # Slot API
    url(r'^slot/play/(?P<game>\d+\.?\d+?)/(?P<bet>\d+\.\d{1,2})/(?P<token>\d+)',
        slot_views.slot_play, name='play'),
    url(r'^slot/reveal/(?P<game>\d+)/(?P<bet>\d+\.\d{2})/(?P<token>\d+)',
        slot_views.slot_view_prize, name='view_prize'),
    url(r'^slot/last_result/(?P<token>\d+)',
        slot_views.slot_last_response, name='last_response'),
    # Account API
    url(r'^account/(?P<token>\d+)',
        slot_views.get_credits, name='get_credits'),
    url(r'^account/login/(?P<pin>\d+)',
        slot_views.login, name='login'),
    url(r'^account/cashout/(?P<token>\d+)',
        slot_views.cashout, name='cashout'),
]
