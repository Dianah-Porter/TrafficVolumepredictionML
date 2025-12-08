from django import forms

class TrafficPredictionForm(forms.Form):
    HOUR_CHOICES = [(i, f"{i}:00") for i in range(24)]
    DAY_CHOICES = [
        (0, 'Mon'),
        (1, 'Tue'),
        (2, 'Wed'),
        (3, 'Thu'),
        (4, 'Fri'),
        (5, 'Sat'),
        (6, 'Sun'),
    ]
    
    hour = forms.ChoiceField(choices=HOUR_CHOICES, label='Hour of Day')
    day_of_week = forms.ChoiceField(choices=DAY_CHOICES, label='Day of Week')
    is_holiday = forms.BooleanField(required=False, label='Is Holiday?')