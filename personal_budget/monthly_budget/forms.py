from django import forms


class TransactionForm(forms.Form):
    date = forms.DateField(input_formats=['%d.%m.%Y'], required=True)
    amount = forms.CharField(required=True)
    description = forms.CharField(required=False)
    outcome = forms.IntegerField(required=False)
    income = forms.IntegerField(required=False)


    def clean(self):
        # Convert date to ISO string
        cleaned_data = super().clean()
        date_iso = self.cleaned_data.get('date').isoformat()
        self.cleaned_data['date'] = date_iso

        # Either 'outcome' or 'income' should be filled, or both
        if not self.cleaned_data.get('outcome') and not self.cleaned_data.get('income'):
            raise forms.ValidationError("Either 'outcome' or 'income' should be filled, or both")

        return cleaned_data
