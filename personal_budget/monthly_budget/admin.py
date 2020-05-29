from django.contrib import admin

from monthly_budget.models import Balance, Category, Period, Transaction

admin.site.register(Balance)
admin.site.register(Category)
admin.site.register(Period)
admin.site.register(Transaction)
