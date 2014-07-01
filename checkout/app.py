from oscar.apps.checkout import app
from django.conf.urls import url, include

from checkout import views


class CheckoutApplication(app.CheckoutApplication):

    def get_urls(self):
        urls = super(CheckoutApplication, self).get_urls()
        urls.append(url(r'^paypal/', include('paypal.express.urls')))
        return urls
    payment_details_view = views.PaymentDetailsView
    shipping_address_view = views.ShippingAddressView
    shipping_method_view = views.ShippingMethodView
    payment_method_view = views.PaymentMethodView


application = CheckoutApplication()
