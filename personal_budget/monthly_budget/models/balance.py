"""Balance model."""

from decimal import Decimal

from django.db import models
from django.db.models import Sum

from .category import Category
from .period import Period
from .transaction import Transaction


class Balance(models.Model):
    """General stats for particular period and category."""

    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    planned_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0)

    def _get_income_amount(self):
        """Calculate income for the period."""
        result = Transaction.transactions.filter(
            period=self.period,
            income=self.category
        ).aggregate(Sum('transaction_amount')).get(
            'transaction_amount__sum'
        )
        return result if result else Decimal('0.00')

    def _get_planned_amount(self):
        """Return planned sum for the period."""
        return self.planned_amount if self.planned_amount else Decimal('0.00')

    def _get_spent_amount(self):
        """Calculate spent sum for the period."""
        result = Transaction.transactions.filter(
            chained_transaction__isnull=True
        ).filter(
            period=self.period,
            outcome=self.category
        ).aggregate(Sum('transaction_amount')).get(
            'transaction_amount__sum'
        )
        return result if result else Decimal('0.00')

    def _get_transferred_amount(self):
        """Calculate transferred sum for the period."""
        result = Transaction.transactions.filter(
            chained_transaction__isnull=False
        ).filter(
            outcome=self.category
        ).aggregate(Sum('transaction_amount')).get(
            'transaction_amount__sum'
        )
        return result if result else Decimal('0.00')

    def export_to_dict(self):
        """Return necessary data."""
        result = {
            'period': str(self.period),
            'category': str(self.category),
            'planned_amount': str(self._get_planned_amount()),
            'income_amount': str(self._get_income_amount()),
            'transferred_amount': str(self._get_transferred_amount()),
            'spent_amount': str(self._get_spent_amount())
        }
        return result
