from django import forms

from .models import ContactMessage

TEXT_INPUT = ('w-full border border-line bg-paper px-4 py-3 text-sm text-ink '
              'outline-none transition-colors focus:border-brass')


class ContactForm(forms.ModelForm):
    # Honeypot: a hidden field real users never fill in (browsers hide it via CSS).
    # Bots that fill it get silently ignored, not spammed into the inbox.
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label='',
    )

    class Meta:
        model = ContactMessage
        fields = [
            'name', 'phone', 'email', 'service', 'agent',
            'preferred_date', 'preferred_time', 'message',
        ]
        labels = {
            'name': 'Full Name',
            'phone': 'Phone',
            'email': 'Email',
            'service': 'Interested In',
            'agent': 'Preferred Agent',
            'preferred_date': 'Preferred Date',
            'preferred_time': 'Preferred Time',
            'message': 'Message (optional)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': TEXT_INPUT, 'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'class': TEXT_INPUT, 'placeholder': 'Your phone number', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': TEXT_INPUT, 'placeholder': 'Your email'}),
            'service': forms.Select(attrs={'class': TEXT_INPUT}),
            'agent': forms.Select(attrs={'class': TEXT_INPUT}),
            'preferred_date': forms.DateInput(attrs={'class': TEXT_INPUT, 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': TEXT_INPUT, 'type': 'time'}),
            'message': forms.Textarea(attrs={
                'class': 'w-full resize-none ' + TEXT_INPUT,
                'rows': 4,
                'placeholder': 'Anything we should know before we meet?',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].empty_label = 'Select one'
        self.fields['agent'].empty_label = 'No preference'