from oscar.apps.partner import strategy, prices
from decimal import Decimal as D


class Selector(object):
    """
    Custom selector to return a FR-specific strategy that charges VAT
    """

    def strategy(self, request=None, user=None, **kwargs):
        return FRStrategy()


class IncludingVAT(strategy.FixedRateTax):
    """
    Price policy to charge VAT on the base price
    """
    # We can simply override the tax rate on the core FixedRateTax.  Note
    # this is a simplification: in reality, you might want to store tax
    # rates and the date ranges they apply in a database table.  Your
    # pricing policy could simply look up the appropriate rate.
    rate = D('0.20')


class FRStrategy(strategy.UseFirstStockRecord, IncludingVAT,
                 strategy.StockRequired, strategy.Structured):
    """
    Typical FR strategy for physical goods.

    - There's only one warehouse/partner so we use the first and only stockrecord
    - Enforce stock level.  Don't allow purchases when we don't have stock.
    - Charge FR VAT on prices.  Assume everything is standard-rated.
    """

    def group_pricing_policy(self, product, variant_stock):
#        stockrecords = [x[1] for x in variant_stock if x[1] is not None]
        #if not stockrecords:
        return prices.Unavailable()
        # We take price from first record
        #stockrecord = stockrecords[0]
        #tax = (stockrecord.price_excl_tax * self.rate).quantize(self.exponent)
        #return prices.TaxInclusiveFixedPrice(
            #currency=stockrecord.price_currency,
            #excl_tax=stockrecord.price_excl_tax,
            #tax=tax)
