from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from oscar.apps.checkout import exceptions
from oscar.apps.checkout.session import CheckoutSessionMixin as OscarCheckoutSessionMixin
from django.utils.translation import ugettext as _

from checkout.utils import CheckoutSessionData


class CheckoutSessionMixin(OscarCheckoutSessionMixin):
    def dispatch(self, request, *args, **kwargs):
        self.checkout_session = CheckoutSessionData(request)
	try:
            self.check_preconditions(request)
        except exceptions.FailedPreCondition as e:
            for message in e.messages:
                messages.warning(request, message)
            return http.HttpResponseRedirect(e.url)
        # call super() from superclass
        return super(OscarCheckoutSessionMixin, self).dispatch(
            request, *args, **kwargs)
    def check_user_cgu(self, request):
        if not self.checkout_session.get_cgu_status():
            raise exceptions.FailedPreCondition(
                url=reverse('checkout:index'),
                message=_("Please accept CGU")
            )
