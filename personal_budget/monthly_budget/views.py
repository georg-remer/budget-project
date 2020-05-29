from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from .forms import TransactionForm
from .models import Category, Period, Transaction


class Main(View):

    def get(self, request, period_id=None):
        form = TransactionForm()
        periods = Period.periods.all().order_by('-beginning')
        categories = Category.objects.all()
        if period_id:
            try:
                period = Period.periods.get(pk=period_id)
            except Period.DoesNotExist:
                raise Http404("Specified period does not exist.")

            dates = Transaction.transactions.filter(
                period=period
            ).distinct(
                'transaction_date'
            )
            transactions = Transaction.transactions.filter(
                period=period
            ).order_by(
                'transaction_date'
            )
        else:
            dates = Transaction.transactions.filter(
                period__in=periods[:1]
            ).distinct(
                'transaction_date'
            )
            transactions = Transaction.transactions.filter(
                period__in=periods[:1]
            ).order_by(
                'transaction_date'
            )
        return render(request, 'monthly_budget/transaction.html', {
            'form': form,
            'periods': periods,
            'categories': categories,
            'dates': dates,
            'transactions': transactions
        })

    def post(self, request, period_id=None):
        form = TransactionForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            transaction = Transaction.transactions.create_transaction(**context)
            period_id = transaction[0].period.pk

            return HttpResponseRedirect(
                reverse(
                    'monthly_budget:main_period',
                    kwargs={'period_id': period_id},
                ),
            )
        return render(
            request,
            'monthly_budget/error.html',
            {'error': form.errors},
        )
