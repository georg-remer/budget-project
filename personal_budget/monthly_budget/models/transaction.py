"""Transaction model."""

from decimal import Decimal

from django.db import models
from django.db.models import Max
from django.db.models import Q

from .category import Category
from .period import Period


class TransactionManager(models.Manager):
    """Provides custom method for transaction creation."""

    def create_transaction(self, **kwargs):
        """Custom data manipulation depending on combination of categories.

        When submitting data on transaction user provides transaction
        amount in absolute form regardless category type - outcome or income.
        E.g. user specifies 100 and chooses income category to write down
        income. Just the same way user specifies 100 (not -100) and chooses
        outcome category to write down how much is spent. 

        Necessery logic is performed automatically substituting 100 with -100
        if outcome is specified, or leaves 100 as it is, if income category
        is specified. In addition to this, 2 transactions are created if
        both are specified at the same time, meaning transferring of amount
        from one category to another.
        """
        # Income
        if kwargs.get('income') and not kwargs.get('outcome'):
            transaction_amount = Decimal(kwargs.get('amount'))
            new_balance = self.get_current_balance(
                Category.objects.get(pk=kwargs.get('income'))
            ) + transaction_amount
            transaction = self.create(
                period=Period.periods.get_or_create_period(kwargs.get('date'))[0],
                income=Category.objects.get(pk=kwargs.get('income')),
                transaction_date=kwargs.get('date'),
                transaction_amount=transaction_amount,
                description=kwargs.get('description'),
                balance=new_balance
            )

            return tuple((transaction,))
        # Outcome
        if not kwargs.get('income') and kwargs.get('outcome'):
            transaction_amount = -Decimal(kwargs.get('amount'))
            new_balance = self.get_current_balance(
                Category.objects.get(pk=kwargs.get('outcome'))
            ) + transaction_amount
            transaction = self.create(
                period=Period.periods.get_or_create_period(kwargs.get('date'))[0],
                outcome=Category.objects.get(pk=kwargs.get('outcome')),
                transaction_date=kwargs.get('date'),
                transaction_amount=transaction_amount,
                description=kwargs.get('description'),
                balance=new_balance
            )

            return tuple((transaction,))
        # Transfer
        if kwargs.get('income') and kwargs.get('outcome'):
            transaction_amount = -Decimal(kwargs.get('amount'))
            new_balance = self.get_current_balance(
                Category.objects.get(pk=kwargs.get('outcome'))
            ) + transaction_amount
            transaction_outcome = self.create(
                period=Period.periods.get_or_create_period(kwargs.get('date'))[0],
                outcome=Category.objects.get(pk=kwargs.get('outcome')),
                transaction_date=kwargs.get('date'),
                transaction_amount=transaction_amount,
                description=kwargs.get('description'),
                balance=new_balance
            )

            transaction_amount = Decimal(kwargs.get('amount'))
            new_balance = self.get_current_balance(
                Category.objects.get(pk=kwargs.get('income'))
            ) + transaction_amount
            transaction_income = self.create(
                period=Period.periods.get_or_create_period(kwargs.get('date'))[0],
                income=Category.objects.get(pk=kwargs.get('income')),
                transaction_date=kwargs.get('date'),
                transaction_amount=transaction_amount,
                description=kwargs.get('description'),
                balance=new_balance
            )

            # Chained transactions
            transaction_outcome.chained_transaction = transaction_income
            transaction_outcome.save()
            transaction_income.chained_transaction = transaction_outcome
            transaction_income.save()

            return transaction_outcome, transaction_income

    @staticmethod
    def get_current_balance(category):
        """Return current balance for the category."""
        latest_transaction_id = Transaction.transactions.filter(
            Q(outcome=category) | Q(income=category)
        ).aggregate(
            Max('id')
        ).get('id__max')
        if latest_transaction_id:
            return Transaction.transactions.get(
                pk=latest_transaction_id
            ).balance
        return Decimal('0.00')

    # @staticmethod
    # def get_latest_date():
    #     latest_transaction_date = Transaction.transactions.aggregate(
    #         Max('transaction_date')
    #     ).get('transaction_date__max')


class Transaction(models.Model):
    """Transaction model."""

    period = models.ForeignKey(Period, on_delete=models.PROTECT)
    outcome = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='outcome',
        null=True
    )
    income = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='income',
        null=True
    )
    chained_transaction = models.OneToOneField(
        'self',
        on_delete=models.CASCADE,
        null=True
    )
    transaction_date = models.DateField()
    transaction_amount = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(null=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2)

    transactions = TransactionManager()

    def __str__(self):
        return "Date: {}, amount: {}, description: {}, outcome: {}, income: {}".format(
            self.transaction_date,
            self.transaction_amount,
            self.description,
            self.outcome,
            self.income,
        )

    def export_to_dict(self):
        """Return necessary data."""
        result = {
            'period': str(self.period),
            'date': self.transaction_date,
            'amount': str(self.transaction_amount),
            'description': self.description,
            'outcome': str(self.outcome) if self.outcome else None,
            'income': str(self.income) if self.income else None,
            'balance': str(self.balance),
        }
        return result
