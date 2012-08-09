#encoding: utf-8
import datetime
from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe

class DateRangeValue(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class DateRangePickerWidget(forms.MultiWidget):
    media = forms.Media(js=[static('js/init_daterangepicker.js')])

    def __init__(self, date_ranges, allow_custom, attrs=None, format=None):
        self.date_ranges = date_ranges
        self.allow_custom = allow_custom

        final_attrs={'class': 'vDateField', 'size':'10'}
        if attrs is not None:
            final_attrs.update(attrs)

        widgets = (
            forms.DateInput(attrs=final_attrs, format=format),
            forms.DateInput(attrs=final_attrs, format=format),
            )
        super(DateRangePickerWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if isinstance(value, DateRangeValue):
            return [self.widgets[0]._format_value(value.start),
                    self.widgets[1]._format_value(value.end)]
        return value

    def format_output(self, rendered_widgets):
        return u'%s - %s' % (rendered_widgets[0], rendered_widgets[1])

    def render(self, name, value, attrs=None):
        date_inputs_html = super(DateRangePickerWidget,self).render(name, value, attrs)

        if not isinstance(value, list):
            value = self.decompress(value)

        range_select_field = '%s_select'
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        local_attrs = self.build_attrs(extra_attrs={'class':'dateRangePicker',
                                                    'style':'display:none;'},
            id=range_select_field % id_)

        if self.allow_custom:
            date_choices = [('- -',u'Custom')]
        else:
            date_choices = []
        for start, end, label in self.date_ranges:
            val = '%s %s' % (self.widgets[0]._format_value(start), self.widgets[1]._format_value(end))
            date_choices.append((val, label))

        selected_value = '%s %s' % (value[0], value[1])

        range_select = forms.Select(choices=date_choices)
        range_select_html = range_select.render(range_select_field % name, selected_value, local_attrs)
        return mark_safe(u'%s %s' % (range_select_html, date_inputs_html))


class DateRangeField(forms.MultiValueField):
    widget = DateRangePickerWidget
    def __init__(self,date_ranges=(), allow_custom=False, format=None, *args,**kwargs):
        fields = (
            forms.DateField(required=True),
            forms.DateField(required=True),
            )

        widget = kwargs.get('widget', self.widget) or self.widget
        if isinstance(widget, type):
            kwargs['widget'] = widget(date_ranges, allow_custom, format=format)

        super(DateRangeField, self).__init__(fields, *args, **kwargs)

    def compress(self,data_list):
        return DateRangeValue(data_list[0], data_list[1])