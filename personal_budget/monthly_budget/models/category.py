"""Category model."""

from django.db import models


class Category(models.Model):
    """Specifies code and name, as well as provider default planned sum."""
    category_code = models.IntegerField(unique=True)
    category_name = models.TextField(unique=True)
    default_planned_sum = models.DecimalField(
        max_digits=9, decimal_places=2, null=True
    )

    def __str__(self):
        return "{}. {}".format(self.category_code, self.category_name)

    class Meta:
        ordering = ['category_code']
        verbose_name_plural = 'categories'
