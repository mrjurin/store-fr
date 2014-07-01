# -*- coding: utf-8 -*-
from decimal import Decimal as D

from oscar.apps.shipping.models import WeightBased, WeightBand
from oscar.apps.shipping import Scales

from oscar.core.loading import get_class

from django.utils.translation import ugettext_lazy as _


class WeightBand(WeightBand):
    pass

class WeightBased(WeightBased):
    """
    Shipping with max weight
    """
    class Meta(WeightBased.Meta):
        abstract = False
        verbose_name = _("Max-Weight-based Shipping Method")
        verbose_name_plural = _("Max-Weight-based Shipping Methods")
    @property
    def charge_incl_tax(self):
        scales = Scales(attribute_code=self.weight_attribute,
                      default_weight=self.default_weight)
        weight = scale.weigh_basket(self._basket)
        band = self.get_band_for_weight(weight)
        if not band:
            if self.bands.all().exists():
                raise Exception("max weight")
            else:
                return D('0.00')
        return band.charge

    @property
    def charge_excl_tax(self):
        return self.charge_incl_tax / D('1.20')

