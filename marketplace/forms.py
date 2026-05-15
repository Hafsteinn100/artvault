from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Bid, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, name=self.cleaned_data['name'])
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image']


class BidForm(forms.ModelForm):
    expiration = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Bid
        fields = ['price', 'expiration']

    def clean_expiration(self):
        expiration = self.cleaned_data['expiration']
        if expiration <= timezone.now():
            raise forms.ValidationError('The expiration date must be in the future.')
        return expiration


COUNTRY_CHOICES = [
    ('Iceland', 'Iceland'),
    ('Denmark', 'Denmark'),
    ('Norway', 'Norway'),
    ('Sweden', 'Sweden'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
]


class FinalizationContactForm(forms.Form):
    street_name = forms.CharField(max_length=255)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=30)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    national_id = forms.CharField(max_length=30, label='National id')


class FinalizationPaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit card'),
        ('bank_transfer', 'Bank transfer'),
        ('wire_transfer', 'Wire transfer'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)
    cardholder_name = forms.CharField(max_length=255, required=False)
    credit_card_number = forms.CharField(max_length=30, required=False)
    expiry_date = forms.CharField(max_length=10, required=False)
    cvc = forms.CharField(max_length=10, required=False)
    bank_account = forms.CharField(max_length=80, required=False)
    sending_bank = forms.CharField(max_length=255, required=False)
    routing_number = forms.CharField(max_length=80, required=False)
    account_number = forms.CharField(max_length=80, required=False)

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        required_fields = {
            'credit_card': [
                'cardholder_name',
                'credit_card_number',
                'expiry_date',
                'cvc',
            ],
            'bank_transfer': ['bank_account'],
            'wire_transfer': ['sending_bank', 'routing_number', 'account_number'],
        }

        for field in required_fields.get(payment_method, []):
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required for the selected payment method.')

        return cleaned_data
