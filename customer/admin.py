from django.contrib import admin
from oscar.core.loading import get_model

CommunicationEventType = get_model('customer', 'CommunicationEventType')
Email = get_model('customer', 'Email')
AnonUserEmailFailure = get_model('customer','AnonUserEmailFailure')


admin.site.register(Email)
admin.site.register(AnonUserEmailFailure)
admin.site.register(CommunicationEventType)
