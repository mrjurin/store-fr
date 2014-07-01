from oscar.apps.customer import abstract_models
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Email(abstract_models.AbstractEmail):
    send_success = models.BooleanField(_("Successful server response"),default=False) 
    last_error = models.TextField(_("Lastest error in sending attemp"),default="",blank=True,null=True)

class AnonUserEmailFailure(models.Model):
    dest = models.EmailField(_('email address'))
    subject = models.TextField(_("Message subject"),default="")
    body = models.TextField(_("Message body"),default="")
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True, null=False)
    def __unicode__(self):
        full_name = 'At : %s To : %s' % (self.date_created, self.dest)
        return full_name.strip()


class CommunicationEventType(abstract_models.AbstractCommunicationEventType):
    pass


class Notification(abstract_models.AbstractNotification):
    pass


class ProductAlert(abstract_models.AbstractProductAlert):
    pass


from oscar.apps.customer.history import *  # noqa
from oscar.apps.customer.alerts.receivers import *  # noqa
