"""Tests for model layer.

This project uses 'active entry' as per Django documentation.
Almost all logic is stored in models, hence, tests aim model layer
first of all.
"""

from django.test import TestCase

from monthly_budget.models import Balance, Category, Period, Transaction
from .test_input import TEST_TRANSACTIONS


class PeriodModelTests(TestCase):
    """Test Period model."""

    def test_get_period_dates(self):
        """
        get_period_dates should return correct period beginning
        and ending for the specified date (ISO format), e.g. 2019-01-01
        as beginning and 2019-12-31 as ending for 2019-12-20.
        """
        tests = {
            '2018-06-01': ('2018-06-01', '2018-06-30'),
            '2019-01-31': ('2019-01-01', '2019-01-31'),
            '2019-02-14': ('2019-02-01', '2019-02-28'),
            '2019-12-20': ('2019-12-01', '2019-12-31'),
            '2020-02-03': ('2020-02-01', '2020-02-29')
        }
        for key, value in tests.items():
            with self.subTest("{}: {}".format(key, value)):
                period_dates = Period.periods.get_period_dates(key)
                self.assertEqual(value, period_dates)

    def test_get_or_create_period_with_existing_periods(self):
        """
        get_or_create_period should return period for the specified date,
        as well as False if returned period was created previously.
        """
        tests = [
            '2018-06-01',
            '2019-01-31',
            '2019-02-14',
            '2019-12-20',
            '2020-02-03'
        ]
        for date in tests:
            with self.subTest(date):
                beginning, ending = Period.periods.get_period_dates(date)
                period_created_beforehand = Period.periods.create(
                    beginning=beginning,
                    ending=ending
                )
                period_to_test = Period.periods.get_or_create_period(date)
                self.assertEqual(
                    period_created_beforehand.id,
                    period_to_test[0].id
                )
                self.assertFalse(period_to_test[1])

    def test_get_or_create_period_with_non_existing_periods(self):
        """
        get_or_create_period should return period for the specified date,
        as well as True if new period has been just created.
        """
        tests = [
            '2018-06-01',
            '2019-01-31',
            '2019-02-14',
            '2019-12-20',
            '2020-02-03'
        ]
        for date in tests:
            with self.subTest(date):
                beginning, ending = Period.periods.get_period_dates(date)
                period_to_test = Period.periods.get_or_create_period(date)
                self.assertEqual(
                    beginning,
                    period_to_test[0].beginning
                )
                self.assertEqual(
                    ending,
                    period_to_test[0].ending
                )
                self.assertTrue(period_to_test[1])


class TransactionModelTests(TestCase):
    """Test Transaction model."""

    fixtures = ['category.json']

    # @classmethod
    # def setUpTestData(cls):
    #     """
    #     Create necessary categories
    #     """
    #     tests = TEST_TRANSACTIONS
    #     for test in tests:
    #         if test['input'].get('outcome'):
    #             Category.objects.get_or_create(
    #                 name=test['input'].get('outcome')
    #             )
    #         if test['input'].get('income'):
    #             Category.objects.get_or_create(
    #                 name=test['input'].get('income')
    #             )

    def test_create_transaction(self):
        """
        create_transaction should create one transaction if outcome
        or income category only is specified, or two transactions,
        if both are specified.
        """
        tests = TEST_TRANSACTIONS
        for test in tests:
            with self.subTest("test #{}".format(test['test_nr'])):
                # Transaction.add_transaction was used when creating
                # transaction using class method. The final way chosen
                # is using instance method in manager.

                # result = Transaction.add_transaction(**test['input'])
                result = Transaction.transactions.create_transaction(
                    **test['input']
                )
                self.assertEqual(
                    test['expected_nr_of_transactions'], len(result)
                )
                result_to_compare = list()
                for value in result:
                    result_to_compare.append(value.export_to_dict())
                self.assertEqual(test['output_transactions'], result_to_compare)


class BudgetModelTests(TestCase):

    fixtures = ['category.json']

    # @classmethod
    # def setUpTestData(cls):
    #     """
    #     Create necessary categories
    #     """
    #     tests = TEST_TRANSACTIONS
    #     for test in tests:
    #         if test['input'].get('outcome'):
    #             Category.objects.get_or_create(
    #                 name=test['input'].get('outcome')
    #             )
    #         if test['input'].get('income'):
    #             Category.objects.get_or_create(
    #                 name=test['input'].get('income')
    #             )

    def test_update_balance(self):
        """
        update_balance should update necessary field for the specified
        category and period
        """
        tests = TEST_TRANSACTIONS
        for test in tests:
            with self.subTest("test #{}".format(test['test_nr'])):
                result_to_compare = list()
                Transaction.transactions.create_transaction(**test['input'])
                period = Period.periods.get_or_create_period(test['input'].get('date'))[0]
                if test['input'].get('outcome'):
                    category = Category.objects.get(
                        pk=test['input'].get('outcome')
                    )
                    balance = Balance.objects.get_or_create(
                        period=period, category=category
                    )[0].export_to_dict()
                    result_to_compare.append(balance)
                if test['input'].get('income'):
                    category = Category.objects.get(
                        pk=test['input'].get('income')
                    )
                    balance = Balance.objects.get_or_create(
                        period=period, category=category
                    )[0].export_to_dict()
                    result_to_compare.append(balance)
                self.assertEqual(test['output_balance'], result_to_compare)
