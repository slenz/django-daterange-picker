django-daterange-picker
=======================

Date range picker for Django

That package contains DateRangePickerWidget and DateRangeField.
DateRangeField is not designed to be saved in the database. Its only for using in the forms.

DateRangeField have attributes:
* _date_ranges_ - list/tuple. Defines selectable date ranges
* _allow_custom_ - boolean. If allow_custom==true, the custom date can be selected.
* _initial_ - get initital start/end date as DateRangeValue

After the form get validated the date range field will contain DateRangeValue. 
This is simple type with start/end dates.


This example of the form uses python-dateutil http://labix.org/python-dateutil/
<pre>
<code>
from datetime import date
from dateutil.relativedelta import relativedelta
from django import forms
from apps.daterangepicker.fields import DateRangeField, DateRangeValue

DATE_RANGES=((date.today() - relativedelta(days=+7),
              date.today(),
              'Last 7 days'),
             (date.today() - relativedelta(months=+1,day=1),
              date.today() - relativedelta(months=+1,day=31),
              'Last month'),
             (date.today() - relativedelta(days=+30),
              date.today(),
              'Last 30 days'),
             (date.today() - relativedelta(years=+1, day=1, month=1),
              date.today() - relativedelta(years=+1, day=31, month=12),
              'Last year'),
             (date.today() - relativedelta(days=+365),
              date.today(),
              'Last 365 days'),
             (date.today() - relativedelta(years=+1, day=1, month=1),
              date.today(),
              'Last and this year'),
             (date.today() - relativedelta(day=1),
              date.today(),
              'This month'),
             (date.today() - relativedelta(day=1, month=1),
              date.today(),
              'This year'))

class MyForm(forms.Form):
    date_range = DateRangeField(label=u'Date range',
        date_ranges=DATE_RANGES,
        initial=DateRangeValue(DATE_RANGES[-1][0],DATE_RANGES[-1][1]),
        allow_custom = True,
        help_text=u'Select date range')
</code>
</pre>

Example of the view:

<pre>
<code>
def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            date_range = form.cleaned_data['date_range']
            start_dt = date_range.start
            end_dt = date_range.end
</code>
</pre>