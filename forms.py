from django import forms
from django.forms.extras.widgets import SelectDateWidget

from snolab_booking.models import Visit, Bed

class VisitForm(forms.Form):
    contact = forms.EmailField(max_length=254) # 254 is recommended in docs
    check_in = forms.DateTimeField(widget=SelectDateWidget)
    check_out = forms.DateTimeField(widget=SelectDateWidget)
    experiment = forms.CharField(max_length=200)
    bed_request = forms.ModelMultipleChoiceField(queryset=Bed.objects.all(), required=False)
    def clean(self):
        super(VisitForm, self).clean()
        check_in = self.cleaned_data.get("check_in")
        check_out = self.cleaned_data.get("check_out")
        if check_out < check_in:
            msg = u"End date should be greater than start date."
            self._errors["check_out"] = self.error_class([msg])
        return self.cleaned_data
