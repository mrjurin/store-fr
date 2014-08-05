from django.conf.urls import url, include
from oscar.app import Shop
from paypal.express.dashboard.app import application as express_dashboard

from checkout.app import application as checkout_app


class StoreFR(Shop):
    checkout_app = checkout_app
#    catalogue_app = get_class('catalogue.app', 'application')
#    customer_app = get_class('customer.app', 'application')
#    basket_app = get_class('basket.app', 'application')
#    checkout_app = get_class('checkout.app', 'application')
#    promotions_app = get_class('promotions.app', 'application')
#    search_app = get_class('search.app', 'application')
#    dashboard_app = get_class('dashboard.app', 'application')
#    offer_app = get_class('offer.app', 'application')
    def get_urls(self):
        urls = super(StoreFR, self).get_urls()
        urls.append(url(r'^dashboard/paypal/express/', include(express_dashboard.urls)))
        urls.append(url(r'^checkout/paypal/', include('paypal.express.urls')))
        return urls

application = StoreFR()
