from django import forms
from core.models import Leave


class LeaveForm(forms.ModelForm):
   
    class Meta:
        model=Leave
        fields=[
            'leave_type',
            'leave_start_date',
            'leave_end_date',
            'leave_start_time',
            'leave_end_time',
            'leave_reason',
        ]
