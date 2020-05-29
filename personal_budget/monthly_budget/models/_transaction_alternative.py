"""Alternative way to create transactions."""

from django.db import models
from django.db.models import Max
from django.db.models import Q

from .category import Category
from .period import Period


class Transaction(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    outcome = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='outcome', null=True)
    income = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='income', null=True)
    date = models.DateField()
    sum = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(null=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return "Date: {}, sum: {}, description: {}, outcome: {}, income: {}".format(
            self.date, self.sum, self.description, self.outcome, self.income
        )

    def export_to_dict(self):
        result = {
            'period': self.period.__str__(),
            'date': self.date,
            'sum': self.sum,
            'description': self.description,
            'outcome': self.outcome.name if self.outcome else None,
            'income': self.income.name if self.income else None,
            'balance': self.balance
        }
        return result

    @classmethod
    def add_transaction(cls, **kwargs):
        # print(kwargs)
        if kwargs.get('income') and not kwargs.get('outcome'):
            transaction = cls(
                period=Period.return_period(kwargs.get('date'))[0],
                income=Category.objects.get(name=kwargs.get('income')),
                date=kwargs.get('date'),
                sum=kwargs.get('sum'),
                description=kwargs.get('description'),
                balance=0
            )
            transaction.balance = Transaction._return_current_balance(
                transaction.income
            ) + transaction.sum
            transaction.save()
            return tuple((transaction,))
        elif not kwargs.get('income') and kwargs.get('outcome'):
            transaction = cls(
                period=Period.return_period(kwargs.get('date'))[0],
                outcome=Category.objects.get(name=kwargs.get('outcome')),
                date=kwargs.get('date'),
                sum=-kwargs.get('sum'),
                description=kwargs.get('description'),
                balance=0
            )
            transaction.balance = Transaction._return_current_balance(
                transaction.outcome
            ) + transaction.sum
            transaction.save()
            return tuple((transaction,))
        elif kwargs.get('income') and kwargs.get('outcome'):
            transaction_outcome = cls(
                period=Period.return_period(kwargs.get('date'))[0],
                outcome=Category.objects.get(name=kwargs.get('outcome')),
                date=kwargs.get('date'),
                sum=-kwargs.get('sum'),
                description=kwargs.get('description'),
                balance=0
            )
            transaction_outcome.balance = Transaction._return_current_balance(
                transaction_outcome.outcome
            ) + transaction_outcome.sum
            transaction_outcome.save()
            transaction_income = cls(
                period=Period.return_period(kwargs.get('date'))[0],
                income=Category.objects.get(name=kwargs.get('income')),
                date=kwargs.get('date'),
                sum=kwargs.get('sum'),
                description=kwargs.get('description'),
                balance=0
            )
            transaction_income.balance = Transaction._return_current_balance(
                transaction_income.income
            ) + transaction_income.sum
            transaction_income.save()
            return transaction_outcome, transaction_income

    @staticmethod
    def _return_current_balance(category):
        latest_transaction_id = Transaction.objects.filter(
            Q(outcome=category) | Q(income=category)
        ).aggregate(
            Max('id')
        )['id__max']
        if latest_transaction_id:
            return Transaction.objects.get(pk=latest_transaction_id).balance
        else:
            return 0
