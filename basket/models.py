from oscar.apps.basket.abstract_models import (
    AbstractBasket, AbstractLine, AbstractLineAttribute)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class InvalidBasketLineError(Exception):
    pass


class Basket(AbstractBasket):
    customer_cgv = models.BooleanField(_("CGV_accept"),default=False)

    def accept_cgu(self,statuts):
        self.customer_cgv = statuts
        self.save()


class Line(AbstractLine):
    pass


class LineAttribute(AbstractLineAttribute):
    pass
