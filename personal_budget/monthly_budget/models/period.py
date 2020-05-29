"""Period model."""

import datetime

from django.db import models


class PeriodManager(models.Manager):
    """Provides necessary methods to manipulate periods."""

    @staticmethod
    def get_period_dates(date):
        """Returns beginning and ending of the month for provider date."""
        date = datetime.date.fromisoformat(date)
        beginning_date = datetime.date(date.year, date.month, 1)
        ending_date = date
        while date.month == ending_date.month:
            ending_date = date
            date += datetime.timedelta(days=1)
        return beginning_date.isoformat(), ending_date.isoformat()

    def get_or_create_period(self, date):
        """Determines actual period and returns it."""
        beginning, ending = self.get_period_dates(date)
        return self.get_or_create(
            beginning=beginning,
            ending=ending
        )


class Period(models.Model):
    """A period is a month with the first and last days stored."""
    beginning = models.DateField(unique=True)
    ending = models.DateField(unique=True)

    periods = PeriodManager()

    def __str__(self):
        return "{0:%Y} {0:%B}".format(
            datetime.date.fromisoformat(str(self.beginning)))
