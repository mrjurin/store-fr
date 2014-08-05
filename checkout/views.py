from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from oscar.apps.checkout import views
from oscar.apps.checkout import mixins
from oscar.apps.payment import forms, models
from oscar.core.loading import get_class

from paypal.payflow import facade

Repository = get_class('shipping.repository', 'Repository')
#CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')

class ShippingAddressView(views.ShippingAddressView): 
    pre_conditions = ('check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured',
                      'check_basket_requires_shipping')
    def post(self, request, *args, **kwargs):
        cgv_accept = self.checkout_session.get_cgu_status() == u"true"
        if not cgv_accept and 'address_id' not in self.request.POST:
            return HttpResponseBadRequest()
        return super(ShippingAddressView, self).post(request, *args, **kwargs)



class ShippingMethodView(views.ShippingMethodView):
    pre_conditions = ('check_basket_is_not_empty',
                      'check_basket_is_valid',
                      'check_user_email_is_captured', )
    def get_available_shipping_methods(self):
        return Repository().get_shipping_methods(
            user=self.request.user, basket=self.request.basket,
            shipping_addr=self.get_shipping_address(self.request.basket),
            request=self.request)

class PaymentMethodView(views.PaymentMethodView):
    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid',
	    'check_user_cgu',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured')
class PaymentDetailsView(views.PaymentDetailsView):
    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured')

    def get_context_data(self, **kwargs):
        # Override method so the bankcard and billing address forms can be
        # added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get(
            'bankcard_form', forms.BankcardForm())
        ctx['billing_address_form'] = kwargs.get(
            'billing_address_form', forms.BillingAddressForm())
        return ctx
    def get(self, request, *args, **kwargs):
        #self.checkout_session.request.basket.customer_cgv = self.checkout_session.get_cgu_status().lower() in ("on","yes", "true", "t", "1",True)
        #self.checkout_session.basket.save()
        s = self.checkout_session.get_cgu_status()
        self.checkout_session.request.basket.accept_cgu(self.checkout_session.get_cgu_status().lower() in ("on","yes", "true", "t", "1",True))
        return super(PaymentDetailsView,self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Override so we can validate the bankcard/billingaddress submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

        bankcard_form = forms.BankcardForm(request.POST)
        billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(),
                    billing_address_form.is_valid()]):
            # Form validation failed, render page again with errors
            self.preview = False
            ctx = self.get_context_data(
                bankcard_form=bankcard_form,
                billing_address_form=billing_address_form)
            return self.render_to_response(ctx)

        # Render preview with bankcard and billing address details hidden
        return self.render_preview(request,
                                   bankcard_form=bankcard_form,
                                   billing_address_form=billing_address_form)

    def do_place_order(self, request):
        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        bankcard_form = forms.BankcardForm(request.POST)
        billing_address_form = forms.BillingAddressForm(request.POST)
        if not all([bankcard_form.is_valid(),
                    billing_address_form.is_valid()]):
            messages.error(request, "Invalid submission")
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Attempt to submit the order, passing the bankcard object so that it
        # gets passed back to the 'handle_payment' method below.
        submission = self.build_submission()
        submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
        submission['payment_kwargs']['billing_address'] = billing_address_form.cleaned_data
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        """
        Make submission to PayPal
        """
        # Using authorization here (two-stage model).  You could use sale to
        # perform the auth and capture in one step.  The choice is dependent
        # on your business model.
        facade.authorize(
            order_number, total.incl_tax,
            kwargs['bankcard'], kwargs['billing_address'])

        # Record payment source and event
        source_type, is_created = models.SourceType.objects.get_or_create(
            name='PayPal')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=total.incl_tax, currency=total.currency)
        self.add_payment_source(source)
        self.add_payment_event('Authorised', total.incl_tax)



class OptInCGV(mixins.OrderPlacementMixin,View):
    pre_conditions = (
        'check_basket_is_not_empty',
        'check_basket_is_valid',
	)
    """
    Opt-In view for fr legal CGV acceptance
    """
    def get(self, request, *args, **kwargs):
        #if 'cgu' in self.request.GET:
            #self.checkout_session.set_cgu_status(self.request.GET.get('cgu',False))
        return HttpResponse("<p>%s</p><p>%s</p><p>%s</p><p> cgu: %s</p><p>%s</p> " % (
                "", #dir(self.checkout_session),
                "", #repr(self.checkout_session.is_shipping_address_set()),
                repr(request.session[u'checkout_data']),
                self.request.GET.get('cgu',False),
                self.checkout_session.get_cgu_status()))
    def post(self, request, *args, **kwargs):
        self.checkout_session.set_cgu_status(self.request.POST.get('cgu',False))
        return HttpResponse("<p>%s</p><p>%s</p><p>%s</p><p> cgu: %s</p><p>%s</p> " % (
                dir(self.checkout_session),
                repr(self.checkout_session.is_shipping_address_set()),
                repr(request.session['checkout_data']),
                self.request.GET.get('cgu',False),
                self.checkout_session.get_cgu_status()))
