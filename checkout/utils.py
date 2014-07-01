from oscar.apps.checkout.utils import CheckoutSessionData as OscarCheckoutSessionData


class CheckoutSessionData(OscarCheckoutSessionData):
    # CGU FR requirements
    def set_cgu_status(self, cgu_status):
        if type(cgu_status) is str:
            cgu_status = cgu_status.lower() in ("yes", "true", "t", "1")
        self._set('cgu', 'status', cgu_status)
    def get_cgu_status(self):
        return self._get('cgu', 'status')
